'''
Bedrock Runtime Client 획득
'''
import boto3
from botocore.config import Config

from app.config import AWS_REGION


def runtime_client():
    """모델 실행용(bedrock-runtime) 클라이언트"""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION,  # boto3는 AWS_REGION이 아니라 AWS_DEFAULT_REGION을 읽으므로 직접 전달
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),  # 스로틀링 시 자동 재시도
    )


get_bedrock_client = runtime_client  # 이전에 쓰던 이름도 그대로 동작하게