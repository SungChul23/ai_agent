'''
- 제시된 임베딩 모델을 이용하여, 텍스트 백터화 변환 처리
- 코사인 유사도 검사를 통해서 유사 문자을 체크
'''

from app.embedding import get_embeddings
from math import sqrt

# 샘플 텍스트
texts = [
    '선수가 먼저, 클럽도 함께’ 모레노의 배려 리더십',
    '감독이 경기 전 선발 명단을 공개하지 않는 것은 특별한 일이 아니다.',
    '선수에게 먼저 설명하고, 몸을 먼저 생각하며, 가진 능력을 최대한 살리는 데 집중하고 있다.'
]
# 3개의 문장을 한번에 임베딩 처리
vectors = get_embeddings().embed_documents( texts )
# 문장별 백터화 길이 체크, 별도 설정 없다면 1024 토큰
print( '차원=>', len(vectors[0]))
print( '차원=>', len(vectors[1]))
print( '차원=>', len(vectors[2]), vectors[2]) # 정규화 처리로 인해 음수 ~ 양수 값으로 배치 -1.0 ~ 1.0 사이로 추정

# 코사인 유사도 -> 두 백터 사이의 거리 계산 (의미가 가까운 문장을 검색활용 -> postgresql에 반영)
# 두 백터가 같은 방향을 가르킨다면 1에 가까와 진다
def cosine_sim(a, b):
    내적     = sum( x*y for x, y in zip(a, b))
    a백터크기 = sqrt( sum( x*x for x in a ) )
    b백터크기 = sqrt( sum( x*x for x in b ) )
    return 내적 / (a백터크기*b백터크기)

print( cosine_sim(vectors[0], vectors[1]) )
print( cosine_sim(vectors[0], vectors[2]) ) # 방향성이 다른 문장에 비해 가깝다.
print( cosine_sim(vectors[1], vectors[2]) )