'''
- 실제 제품과 대상을 제시하여, LLM이 홍보 문구를 구성하는 서비스 수행
- 프럼포트는 사전에 준비된 구성(ROLE, ... 제약)에 맞춰서 동적 생성 및 LLM 전달
'''
import json

from app.bedrock import runtime_client
from app.config import BEDROCK_CHAT_MODEL_ID
from app.prompts import marketing_prompt

# 프롬포트 구성 함수를 이용하여 동적 생성
# 파라미터 - 제품 / 대상
prompt = marketing_prompt("AI 고객 상담 솔루션", "온라인 쇼핑물 CS팀")

print(prompt)

response = runtime_client().converse(
    modelId=BEDROCK_CHAT_MODEL_ID,
    messages=[{"role": "user", "content": [{"text": prompt}]}],

    inferenceConfig={"maxTokens": 600},
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