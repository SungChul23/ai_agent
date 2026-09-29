'''
- data/~ 에 존재하는 데이터를 읽기 -> 메타데이터, 텍스트 분리 -> 텍스트 청킹 -> 디비 입력
- 메타데이터는 md 파일 구조로 처리하여 디비 입력
'''

from app.ingestion.ingest import main

main()