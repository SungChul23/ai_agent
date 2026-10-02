'''
rag 검색 성능 테스트 진행
'''

from app.evaluation.retrieval_eval import main

# 테스트 데이터를 검색 => top-k개의 검색 결과에 모두 기대 문서가 포함되었는지 카운팅
main(5)