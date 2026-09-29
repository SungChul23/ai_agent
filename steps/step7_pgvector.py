'''
텍스트 -> 임베딩 하여 생성된 백터 데이터를 PostgreSQL pgvector에 저장하고, 유사도 검색 SQL 실행
'''

# 1. 모듈 가져오기
from pgvector import Vector
from app.embedding import get_embeddings
from app.database import connect

# 2. 검색어로 사용될만한 샘플 문장 준비 (hr, sales, cs)
samples = ["환불 정책","연차 휴가 규정","월 매출 분석"]

# 3. 임베딩 : [ [...], [...], [....(1024)]]
vectors = get_embeddings().embed_documents( samples )

# 4. 디비 쿼리 수행
with connect() as conn, conn.cursor() as cur: # with문 2개 사용한것과 같은 결과
    # 데이터 : 원문 텍스트, 임베딩된 백터
    for text, vec in zip( samples, vectors): # 순서대로 쌍으로 묶어서 하나씩 꺼냄
        #print( text, vec )
        # sql 수행
        cur.execute("""
            insert into demo_vectors(content, embedding) values (%s, %s)
            on conflict(content)
            do update set embedding=EXCLUDED.embedding
        """, (text, Vector(vec) ) )
        #break
    conn.commit()
    pass

# 5. 유사도 검사 (질문백터 <-> DB상에 적제된 데이터 백터간 거리를 측정)
# 5-1. 질문의 백터화
q = get_embeddings().embed_query('상품을 반품하고 싶어요') # cs 관련 질문
with connect() as conn, conn.cursor() as cur:
    # <=> : 코싸인 유사도 계산 연산자 (pgvector 제공) 
    # embedding <=> %s : 유사도 측정 표현
    # 계산값이 작으면 -> 서로 비슷하다
    # 양적으로 표현 : (1-유사도) => 값이 클수록 유사도가 높다라고 표현
    cur.execute("""
        select
            content,
            1-(embedding <=> %s) score
        from
           demo_vectors 
        order by embedding <=> %s 
        limit 3
    """, (Vector(q), Vector(q)) )
    # 결과 출력
    for result in cur.fetchall():
        print( result )