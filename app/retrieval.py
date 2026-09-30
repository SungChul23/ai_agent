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
    '''
    sql = f"""
        select
            d.document_code,
            d.title,
            d.department,
            d.category,
            c.content,
            1-(c.embedding <=> %s) as vector_score,
            ts_rank(
            
            ) as score

        from document_chunks c 
        join documents d
        on c.document_id=d.id
        order by (c.embedding <=> %s)
        limit %s
    """