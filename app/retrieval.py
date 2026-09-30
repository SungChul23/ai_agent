'''
- postgresql + pgvector를 이용하여 백터 데이터를 검색, 유사도등 진행
- 백터 검색, 메타데이터 필터링, 하이브리드 서치 기능까지 확장
'''

from pgvector import Vector
from app.database import connect
from app.embedding import get_embeddings

def vector_search(query:str, k:int=5):
    # 1. 사용자 질문 임베딩 -> 백터 변환 처리
    q = Vector( get_embeddings().embed_query(query) )
    
    # 2. 디비 커넥션, 커서 획득
    results = None
    with connect() as conn, conn.cursor() as cur:
        # 질문과 청킹 처리된 임베딩 데이터와 비교하여 유사도 계산 => (1-유사도), 정렬, 상위 k개만큰 반환
        # documents 에서는 문서코드, 제목, 부서, 카테고리, 
        # join
        # document_chucks에서는 원문콘텐츠, (1-유사도) score
        cur.execute("""
            select
                d.document_code,
                d.title,
                d.department,
                d.category,
                c.content,
                1-(c.embedding <=> %s) as score
            from document_chunks c 
            join documents d
            on c.document_id=d.id
            order by (c.embedding <=> %s)
            limit %s
        """, (q, q, k))
        results = cur.fetchall()
    return results


def advanced_search(
    query:str, 
    department:str | None = None,
    category:str | None = None,
    k:int=5
):
    '''
    - 백터검색 + 메타데이터 필터링 + 키워드 결합한 검색 (RDB + 백터디비 장점 혼용)
    '''
    # 1. 사용자 질문 임베딩
    q = Vector( get_embeddings().embed_query(query) )
    
    # 2. 필터링 관련, 키워드(파라미터) 모름 리스트
    filters, params = [], []

    # 3. department 존재하면
    if department:
        filters.append("d.department=%s")
        params.append(department.upper())  # 원문 대문자

    # 4. category 존재하면
    if category:
            filters.append("d.category=%s")
            params.append(category.lower()) # 원문 소문자

    # 5. 조건 쿼리 구성
    where = ("where " + " AND ".join(filters)) if filters else ""

    # 6. sql 구성
    '''
        # CTE(Common table expression) 구조, 서브쿼리를 사용했다 비교 유사
        with scored as (
            select ...
        )
        select ...
        from scored
        
        # PostgreSQL의 FTS(Full Text Search)를 이용한 키워드 일치 점수 산출 기능
        # ts_rank() : [v]문서와 검색어가 얼마나 잘 일치하는지 점수로 계산
        # to_tsvector() : 문서 내용을 검색 가능한 토큰 형태로 변환. 'simple' 보편적인 언어 대상, 'english' 등 존재
        # plainto_tsquery() : 사용자가 입력한 일반 문자열을 PostgreSQL의 검색 Query 형태로 변환

        # 하이브리드 검색 + 키워드 검색
        # 유사도 점수(80%), FTS(20%) 점수를 블랜딩 처리 => 보다 정확한 의미를 가징 정보 추출 + 키워드(부서,카테고리)

        # LEAST(fts_score, 1.0)*0.2 : 둘중 더 작은 값을 선택 0.0 <= LEAST(fts_score, 1.0) <=0.2
    '''
    sql = f"""
        with scored as (
            select
                d.document_code,
                d.title,
                d.department,
                d.category,
                c.content,
                1-(c.embedding <=> %s) as vector_score,
                ts_rank(
                    to_tsvector('simple', c.content),
                    plainto_tsquery('simple', %s)
                ) as fts_score
            from document_chunks c 
            join documents d
            on c.document_id=d.id
            {where}
        )

        select
            document_code,
            title,
            department,
            category,
            content,
            vector_score,
            (vector_score*0.80 + LEAST(fts_score, 1.0)*0.20  ) as hybrid_score
        from scored
        order by hybrid_score desc
        limit %s
    """
    # [백터화 된 질문, 오리지널 질문 텍스트, 동적으로 구성되는 키워드들, 최대 1 ~ 20개 구성|k개 ]
    total_params = [q, query, *params, max(1, min(k, 20) )]

    with connect() as conn, conn.cursor() as cur:
        cur.execute( sql, total_params )
        return cur.fetchall()