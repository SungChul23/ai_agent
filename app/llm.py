'''
랭체인에서 사용할 bedrock 전용 chat model 객체 생성
- 기존 aws api 사용
- 이후 랭체인 api 사용
'''

from langchain_aws import ChatBedrockConverse
from .config import AWS_REGION, BEDROCK_CHAT_MODEL_ID

# 랭체인 API를 이용하여 aws bedrock 모델 호출(객체 생성 및 재사용) vs 이전 코드까지는 boto3 api 사용 llm 호출
def get_chat_model():
    return ChatBedrockConverse(
        model=BEDROCK_CHAT_MODEL_ID,
        region_name=AWS_REGION,
        max_tokens=1200,
    )