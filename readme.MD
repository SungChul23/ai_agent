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
# 맥
source agent/Scripts/activate

(agent) ...>

# 필요 패키지 설치
(agent) ..> pip install -r requirements.txt
```

# Bedrock API 키 발급
- 30일짜리 장기키 발급 (단 리전은 버지니아에서 진행)

# 환경 설정 파일
- .env
```
# .env.example 카피하여 구성
# 추가, 뒤에 api는 별도 발급(Bedrock API 키 발급)하여 세팅
AWS_BEARER_TOKEN_BEDROCK=
```

# 임베딩모델
- 텍스트 => 백터화시 사용하는 토크나이저
- 기본(최대 크기) 1024 토큰
- 모델 : amazon.titan-embed-text-v2:0
```
https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/model-catalog/serverless/amazon.titan-embed-text-v2:0
```

# PC에 세팅된 리전 조정
```
# 확인
aws configure get region

# 버지니아 조정
aws configure set region us-east-1
```

# 본 프로젝트 남은 내용
- agent-loop
    - 에이전트 사용 > 결과를 검증, 재시도 루프 구조

- 하네스 엔지니어링
    - 에이전트 실행에 대한 정책 계층 구성
        - 툴 사용, 실행 버짓, 프럼프트 인젝션 방어, 테스트 코드 분리
        - LLM의 성능, 권한, 예산, 실패등등 경계를 명확하게 구성 

- 클라우드 서비스 반영
    - 테라폼을 통한 인프라구성, postgresql -> RDS
    - 로컬에서 구성한 서비스를 클라우드로 마이그레이션 진행

- 프로젝트 형태 마무리