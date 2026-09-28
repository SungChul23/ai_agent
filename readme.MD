# 목표
- LLM API 사용(bedrock 사용)
- Agent, A2A, 자율형 Agent 개발
- MCP 개발, 이를 통해 외부 도구 사용 (대부분 개발되어 있음)
- RAG 사용 (데이터=> 백터디비(fiass, postgreSQL+extension) 저장, 토크나이저 사용)
- 브런치 계속 확장 -> 목표 프로그램 도달
- 랭체인, 랭그래프, 랭스미스 제품 활용 (에이전트 개발, 서비스 모니터링/관리 등 사용)

# 기본 가상환경 구성
```
# 가상환경 구성
python -m venv agent

# 활성화
# 윈도우
agent\Scripts\activate
./agent/Scripts/activate.bat

(agent) ...>

# 필요 패키지 설치
(agent) ..> pip install -r requirements.txt
```

# 환경 설정 파일
- .env
```

```

# 임베딩모델
- 텍스트 => 백터화시 사용하는 토크나이저
- 기본(최대 크기) 1024 토큰
- 모델 : amazon.titan-embed-text-v2:0
```
https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/model-catalog/serverless/amazon.titan-embed-text-v2:0
```