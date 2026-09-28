'''
Bedrock LLM 호출 테스트 (Converse API)
'''
import json

from app.bedrock import runtime_client
from app.config import BEDROCK_CHAT_MODEL_ID

# 1. 런타임 클라이언트 획득
client = runtime_client()

# 2. LLM 호출
response = client.converse(
    modelId=BEDROCK_CHAT_MODEL_ID,
    messages=[{"role": "user", "content": [{"text": "AI Agent를 5줄로 설명해줘."}]}],
    # temperature 등 샘플링 옵션은 이 모델이 거부하므로 넣지 않음
    inferenceConfig={"maxTokens": 2000},
)

# 3. 응답 구조 확인 (진단용)
blocks = response["output"]["message"]["content"]
print("stopReason :", response["stopReason"])
print("usage      :", response["usage"])
print("block types:", [list(b.keys())[0] for b in blocks])
print("-" * 40)

# 4. 위치([0])가 아니라 text 블록만 골라서 읽기
text = "".join(b["text"] for b in blocks if "text" in b)

if text:
    print(text)
else:
    print("텍스트 블록이 없습니다. 원본 content:")
    print(json.dumps(blocks, ensure_ascii=False, indent=2, default=str))