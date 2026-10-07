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
```

# 인프라구성
```
# 초기화
terraform init
# 포멧팅
terraform fmt
# 유효성 검사
terraform validate
```