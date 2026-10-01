'''
- @tool 이 붙은 함수의 내부 1번 라인에는 함수 주석(doc-string) 을 반드시 기재, 함수의 역활 명확하게 기술->LLM이 판단하는 재료
- 도구 (2개)
    - 사용자가 명시한 지속적인 신호, 업무 방식을 장기 기억으로 저장 도구 함수
    - 현재 질문과 관련된 사용자의 과거 장기 기억을 검색하는 도구 함수
'''
# 1. 모듈 가져오기
from langchain_core.tools import tool
from app.database import connect
from app.embedding import get_embeddings
from app.config import USER_ID # 임시용, 사용자를 구분하는 값
from pgvector import Vector

# 2. 도구 1
@tool
def remember_user_preference(content: str, importance: float=0.7) -> str:
    '''
        사용자가 명시한 지속적인 신호, 업무 방식을 장기 기억으로 저장한다.
    '''
    # 파라미터 구성
    # content -> 임베딩후 백터화 처리
    vec = Vector( get_embeddings().embed_query(content) )
    # 중요도 보정
    importance = max(0.0, min(float(importance), 1.0))

    # 쿼리 실행
    with connect() as conn, conn.cursor() as cur:
        # insert 구문
        sql = """
            insert into agent_memories
            (used_id, memory_type, content, embedding, importance)
            values
            (%s,'preference', %s, %s, %s)
        """
        params = (USER_ID, content, vec, importance)
        cur.execute( sql, params )
        conn.commit()
    return "preference memory saved" # 도구를 사용한 LLM에게 전달 (랭그래프 설계상 툴 => Agent )

# 3. 도구 2
@tool
def recall_user_memory(query: str, k: int=3) -> str:
    '''
        현재 질문과 관련된 사용자의 과거 장기 기억을 검색한다.
    '''
    # 파라미터 구성
    q = Vector( get_embeddings().embed_query(query) )
    # 검색 결과 개수 (1~5개 제한)
    k = max(1, min(k, 5))    
    # 쿼리 실행
    with connect() as conn, conn.cursor() as cur:
        # select 구문
        sql = """
            select
                id, memory_type, content, importance, 1-(embedding <=> %s) as score
            from agent_memories
            where used_id=%s
            order by embedding <=> %s
            limit %s
        """
        params = (q, USER_ID, q, k)
        cur.execute( sql, params )
        # 결과셋 모두 가져오기
        rows = cur.fetchall()
        # 엑세스 시간 update 구문 -> 결과셋으로 나온 항목만 대상
        if rows:
            cur.execute("""
                update
                    agent_memories
                set
                    last_accessed_at=NOW()
                where 
                    id=ANY(%s)
            """, ([row[0] for row in rows], ) )
            conn.commit()
        pass

    # 검색 결과를 문자열로 구성하여 타입, 유사도점수, 중요도, 내용을 k개 반복 구성하여 반환
    # 도구를 사용한 LLM에게 전달 (랭그래프 설계상 툴 => Agent )
    return "\n".join( f"[{typ} score={score:.3f} importance={imp}] {content}" for _, typ, content, imp, score in rows ) or "관련 기억 없음"