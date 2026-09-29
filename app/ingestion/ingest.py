'''
- 업무 문서를 chunking->embedding->PostgreSQL/pgvector 적제
- RAG에서 사용하는 지식 베이스 구성에 대한 Ingestion pipeline
'''
from pathlib import Path
from .loader import load_markdown
from .splitter import splite_text
from app.embedding import get_embeddings
from app.database import connect
from pgvector import Vector
from psycopg.types.json import Jsonb

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
#print( DATA )
# rglob() : `하위` 경로까지 다 찾아가서 해당 파일을 찾는다
#print( DTAA.rglob("*.md") )

# md 파일 별로 처리
def ingest_file( path: Path):
    # 1. 문서내에서 메타 데이터와 본문 분리(혹은 로드) -> '---' 기준 분할
    meta, body = load_markdown( path )
    #print( meta )
    #print( '-'*30 )
    #print( body )

    # 2. body(규약 원문) 관련 rag에서 검색 가능한 작은 단위로 chunk 처리 (fixed-size 단순 청킹 수행)
    #    300 글자수로 청킹을 하니 시멘틱이 나름대로 잘 섹션화된듯 => 트레이트 오프상 최적 청킹 기준으로 판단 할수 잇을듯(예상)
    chunks = splite_text(body, 300)
    #print( chunks )

    # 3. 임베딩 처리
    vectors = get_embeddings().embed_documents( chunks )

    # 4. 메타데이터, 백터 를 데이터베이스에 입력 -> 하나의 트렌젝션으로 관리
    #    documents, document_chunks 각각 테이블에 입력
    with connect() as conn, conn.cursor() as cur:
        # 1회 documents 저장, upsert
        # insert에 입력하고자 했던 값은 => EXCLUDED.xxx
        cur.execute("""
            insert into documents 
            (document_code, department, category, title, source, version, effective_date)
            values
            (%s, %s, %s, %s, %s, %s, %s)
            on conflict(document_code)
            do update set
                department=EXCLUDED.department,
                category=EXCLUDED.category,
                title=EXCLUDED.title,
                source=EXCLUDED.source,
                version=EXCLUDED.version,
                effective_date=EXCLUDED.effective_date
            returning id
        """, (meta['document_code'],meta['department'],meta['category'],meta['title'],str(path.relative_to(ROOT)), meta.get('version'),meta.get('effective_date')))
        # 참조키
        document_id = cur.fetchone()[0]
        # 같은 문서로 저장된 청크가 존재한다면 -> 삭제
        # delete
        cur.execute('delete from document_chunks where document_id=%s', (document_id,))
        # n회 document_chunks 저장
        for i, (chunk, vector) in enumerate( zip(chunks, vectors) ):
            # 청크별로 추가로 메타 정보 설정 (소스(원본문서), 부서, 내용카테고리)
            chunk_meta = {
                "section_source": path.name,
                "department":     meta['department'],
                "category":       meta['category']
            }
            # insert into document_chunks ...
            # Jsonb : 파이썬의 dict/list 데이터를 postgreSQL의 jsonb 타입으로 변화 처리
            cur.execute("""
                insert into document_chunks 
                (document_id, chunk_index, content, embedding, metadata)
                values
                (%s, %s, %s, %s, %s)
            """, (document_id, i, chunk, Vector(vector), Jsonb(chunk_meta)))

        # 커밋
        conn.commit()
        pass
    pass

def main():
    # 파일별 처리 구성
    for path in sorted(DATA.rglob("*.md")):
        print( path )
        ingest_file( path )
        #break
    pass

if __name__ == "__main__":
    main()