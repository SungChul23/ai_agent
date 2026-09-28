'''
프로그램 전체 환경변수 로드, 관리
'''

import os
from dotenv import load_dotenv

load_dotenv()  # .env → 프로세스 환경변수로 등록 (getenv보다 먼저)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_CHAT_MODEL_ID = os.getenv("BEDROCK_CHAT_MODEL_ID")
BEDROCK_EMBEDDED_MODEL_ID = os.getenv("BEDROCK_EMBEDDED_MODEL_ID")
DATABASE_URL = os.getenv("DATABASE_URL")

# 필수 값이 없으면 호출 단계까지 가지 말고 여기서 바로 알려줌
if not BEDROCK_CHAT_MODEL_ID:
    raise RuntimeError("BEDROCK_CHAT_MODEL_ID가 .env에 없습니다.")