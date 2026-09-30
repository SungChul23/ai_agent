# 목표
- 문단 단위 청킹, 시멘틱 청킹 
- 메타데이터 필터링
- 벡터 + 키워드 하이브리드 검색 (추론시 비율로 활용)

# 시멘틱 청킹
- 말뭉치 -> 분절 (문장/문단 단위 (단순하게 구성 : . ! ? ...  )) -> 단 단위별 임베딩 -> 인접에 대한 유사도 계산 (앞뒤 백터간 유사도 계산) -> 유사도가 특정 임계값보다 낮아지는 지점 체크 + 최소 토큰(문자)수 -> 청킹
- 유사도가 높은 문장/문단간 청킹 진행
- 임계값이 최적화는 다른문제 -> 차후 추론등 과정을 통해서 평가 진행 (최적 청킹 대한 평가)
- 임계값은 임시 설정
    - 변수 : 임베딩 모델, 문서(말뭉치 원소스)의 구성와 특성, 임계값, 사용(추론행위) -> 평가

# 구조
```
/
L app
    L ingestion
        L ingest.py     : 업그레이드
        L splitter.py   : 업그레이드
    L retrieval.py      : 업그레이드
L steps
    L step10_rag_advanced.py : 신규
```

# 실행
```
python -m steps.step10_rag_advanced
```

# 시멘틱 청킹 후 db에 입력
- app.ingestion.ingetst.py 수정
    - 청킹의 종류별로 사용할수 있는 상위 함수 구성
    - 데이터를 구축 하는 부분에 함수 대체
```
# 최종 실행
python -m steps.step8_document_ingestion

# psql 접속후 
---
select 
    id, document_id, chunk_index, 
    left(content, 10) || '...' as content,
    left(embedding::text, 10) || '...' as embedding,
    metadata
from 
    document_chunks
order by id;

#  문단 단위 기준 대비 청킹 숫자가 변화됨을 확인
```