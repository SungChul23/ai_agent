# 목표
- 운영상에 세밀한 평가 및 랭체인, 랭그래프 운영 모니터링등 추적하기 위한 장치 필요
    - 랭스미스 설정

# 세팅
- 랭스미스 가입
    - https://smith.langchain.com/ > 가입 > 로그인
    - 대시보드 > 앱선택 > tracing > + Project 클릭 > "ai-agent" 입력후 생성
        - 키 생성 버튼 사용 => .env 카피
            ```
                LANGSMITH_TRACING=true
                LANGSMITH_ENDPOINT=https://api.smith.langchain.com
                LANGSMITH_API_KEY=...
                LANGSMITH_PROJECT="ai-agent"
            ```

# 구조
```
/
L steps
    L step18_observability.py
L app
    L observability.py            : 랭스미스 상태 반환
```

# 실행
```
python -m steps.step18_observability
```