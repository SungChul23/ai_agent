'''
프로그램 전체 환경변수 로드, 관리
'''

import os
from dotenv import load_dotenv


# 환경변수 로드
load_dotenv()

# 변수로 사용
# .env -> load_dotenv() -> os.getenv("ENV_VAR_NAME")
AWS_REGION                = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_CHAT_MODEL_ID     = os.getenv("BEDROCK_CHAT_MODEL_ID")
BEDROCK_EMBEDDED_MODEL_ID = os.getenv("BEDROCK_EMBEDDED_MODEL_ID")
DATABASE_URL              = os.getenv("DATABASE_URL")