'''
bedrock 임베딩 모델을 생성, 재사용 모듈
텍스트 입력 -> 백터로 변환 처리시 사용할 수 있다
'''
from langchain_aws import BedrockEmbeddings
from .config import AWS_REGION, BEDROCK_EMBEDDED_MODEL_ID

# 싱글톤 스타일로 구성
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        # 최초 1회만 초기화
        _embeddings = BedrockEmbeddings(model_id=BEDROCK_EMBEDDED_MODEL_ID, region_name=AWS_REGION)
    return _embeddings