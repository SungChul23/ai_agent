'''
Bedrock LLM Call 테스트
'''

from app.bedrock import get_bedrock_client
from app.config import BEDROCK_CHAT_MODEL_ID

# 1. Bedrock Client 획득
bedrock_client = get_bedrock_client()

# 2. LLM Call
resp = bedrock_client.converse(
    modelId=BEDROCK_CHAT_MODEL_ID,
    messages=[{"role": "user", "content": [{"text": "안녕"}]}],
    system=[{"text": "너는 친절한 도우미야"}],
    inferenceConfig={"maxTokens": 2000}, 
)

# 3. 응답 결과 파싱, 출력
print(resp["output"]["message"]["content"][0]["text"])