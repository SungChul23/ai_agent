# 목표
- agent를 백엔드 서비스 구성
    - fastapi 사용
        - dokerfile 구성
        - 소스코드 같이 구성 배포 (ci/cd x)
    - postgresql (임시 도커 or rds)
- cloud에 배포/배치
- 기존 코드 최대한 유지 -> 컨테이너-> 인프라자동화 -> 배포

# 구조
```
/
--- 서비스 관점(백엔드)
L app
    L [v] main.py    : Agent를 fastapi에서 가급적 공용으로 실행하도록 함수 추가(보정)
    L [v] service.py : fastapi로 백엔드 구성, /chat, /health
L steps
    L [v] step21_agent_service.py : 로컬에서 fastapi 구동
--- 도커
L [v] requirements.txt            : fastapi, uvicorn 추가
L Dockerfile                  : 에이전트 구동하는 컨테이너 이미지
L docker-compose.yml          : 수정, 2개 서비스 (postgreSQL, agent service)

--- 인프라
L infra
    L scripts
        L bootstrap.sh
        L bootstrap.bat     : ec2(인프라) 자동 배포 구성
    L terraform             
        L *.tf              : 인프라 구성용 (버지니아 리전 사용)
```


# 로컬 실행
```
python -m steps.step21_agent_service
---
http://localhost:8000/docs 접속
- url 별로 테스트 진행 (프럼트 페이지 없이 사용 가능 -> 향후 slack/텔레그램등 기타서비스 담당)
    - /chat  : `try it out` -> 프럼프트 구성하여 질문후 execute 버튼 클릭
    - /heath : `try it out` -> execute 버튼 클릭
```

# Agent 컨테이너화
- Dockerfile 구성하여 이미지 생성
    - Fastapi + 랭그래프등

# 도커 컴포즈 구성
- 서비스
    - Agent 컨테이너 추가
- 컨테이너 구성
    - DATABASE_URL: postgresql://agent:agent@postgres:5432/agentlab
    ```
        docker compose up --build
    ```

# 인프라 구성
```
versions.tf     : 필요한 provider 추가
provider.tf     : 필요한 provider의 세부 설정 -> aws 리전
variables.tf    : tf 구성에 필요한 모든 변수들 설정

network.tf      : VPC 구성 (VPC->public subnet 2개 -> Route Table -> IGW -> 외부) + 가용영역에 서브넷 배치
                  EC2 public subnet 개방, RDS public subnet 배치되지만 EC2에서만 접근 제한

security.tf     : 보안그룹 구성(방화벽등), ec2, rds

rds.tf          : RDS + 백터디비 관련 구성
                  비번자동생성, 접속URL 자동구성 => SSM에서 전달하도록  KMS에 저장 구조
                  코드,tf 파일에 db 비번 x

deploy.tf       : 애플리케이션 배포
                  현대프로젝트=>ZIP압축=>비공개 s3 버킷 업로드
                  차후 bootstrap.sh이 ZIP을 내려 받아서 Docker Image 구성

iam.tf          : ec2 role 구성, 필요권한 정책 부여

ec2.tf          : Amazon Linux 2023 ec2 구성, bootstrap.sh로 user_data 전달 처리
                  인프라 생성후 실제 서비스 자동 설치/DB 초기화(sql 마이그레이션(테이블 생성=> 데이터 삽입))/컨테이너 실행
```

# 인프라구성 (CI/CD 배제, 에이전트 API만 구성, 비용 최소로 구성(RDS 비용, ec2 최소,vpc 비용))
```
# 초기화
terraform init
# 포멧팅
terraform fmt
# 유효성 검사
terraform validate

# 설치
terraform apply
---
Outputs:

api_url = "http://3.239.208.60:8000"
chat_url = "http://3.239.208.60:8000/chat"
ec2_public_ip = "3.239.208.60"
health_url = "http://3.239.208.60:8000/health"
rds_endpoint = "agent-de-ai-30-postgres.c43ekyi6yiie.us-east-1.rds.amazonaws.com"
ssm_connect_command = "aws ssm start-session --target i-0e6c91d038b198857 --region us-east-1"

# 테스트 (2분후 진행)
- http://3.239.208.60:8000/docs 접속
- /chat 선택 -> try it out -> 파라미터 수정
    ```
        `{
            "message": "2026년 9월 판매현황 알려줘"
         }
    ```
- execute 버튼 클릭 -> 에이전트 작동 -> 
    ```
        {
            "answer": "## 📊 2026년 9월 판매현황 (2026-09-01 ~ 2026-09-30)\n\n### 전체 요약\n| 항목 | 값 |\n|---|---|\n| 총 매출 | 3,586,000원 |\n| 총 주문 건수 | 8건 |\n| 평균 주문 단가 | 약 448,250원 |\n\n### 매출 상위 제품 TOP 5\n| 순위 | 제품명 | 판매수량 | 매출액 |\n|---|---|---|---|\n| 1 | 사내 AI Agent 구축 | 1 | 1,200,000원 |\n| 2 | RAG 구축 컨설팅 | 1 | 800,000원 |\n| 3 | 데이터 분석 패키지 | 4 | 600,000원 |\n| 4 | AI 업무자동화 Pro | 6 | 594,000원 |\n| 5 | AI 업무자동화 Basic | 8 | 392,000원 |\n\n인사이트: 매출 1위는 '사내 AI Agent 구축' 건으로, 단건이지만 전체 매출의 약 33.5%를 차지합니다. 'AI 업무자동화 Basic'은 판매 수량(8개)이 가장 많지만, 단가가 낮아 매출 비중은 상대적으로 작습니다.\n\n추가로 동일 기간 환불 현황이나 전월 대비 비교가 필요하시면 말씀해주세요.",
            "sources": [
                "sales_summary 도구 결과",
                "top_products 도구 결과"
            ],
            "tools_used": [
                "sales_summary",
                "top_products"
            ],
            "confidence": 0.85
        }
    ```
```