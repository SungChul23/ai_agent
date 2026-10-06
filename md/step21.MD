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
    L main.py    : Agent를 fastapi에서 가급적 공용으로 실행하도록 함수 추가(보정)
    L service.py : fastapi로 백엔드 구성, /chat, /health
L steps
    L step21_agent_service.py : 로컬에서 fastapi 구동
--- 도커
L requirements.txt            : fastapi, uvicorn 추가
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