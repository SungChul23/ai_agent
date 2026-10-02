'''
- RAG 검색 성능을 MRR, 일치되면 히트수 기준으로 평가
- advanced_search() 성능 테스트
    - 성능표 구성하여 기준에 미달하면, 비율 조절(8:2 => 7:3등 미세조정을 통해서 검색 정확도 상승)
'''

# 1. 데이터셋
from app.evaluation.dataset import CASES
# 2. 검색
from app.retrieval import advanced_search

# 성능평가
# Top-K 검색 결과에 질문에 대한 기대문서가 포함되었느지 체크
def main(k:int = 5):
    # 결과를 담는 그릇
    # hits : 기대 문서가 Top-k 검색 결과에 포함되었느지 기록
    # reciprocal : 기대 문서의 검색 순위에 대한 역순위 기록 (1/rank)
    hits, reciprocal = list(), list()

    for case in CASES:
        # 1. 질문과 k를 세팅해서 문서 검색 (RAG)
        rows = advanced_search( case['question'], k=k)

        # 2. 결과에서 문서 코드만 추출
        #    row[0] : 결과셋의 첫번째 컬럼이 문서코드임
        codes = [ row[0] for row in rows ]

        # 3. 기대 정답(문서코드) 획득
        expected = case['expected_source']

        pass

    pass

# 직접 실행 대비
if __name__ == '__main__':
    main()