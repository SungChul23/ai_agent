# 목표
- 최종 응답 결과를 단순 문자열등 처리하지 않고, 구조화 하여 처리
- 대답/소스/툴사용/컨피던스 등 형태에 맞춰 응답값 세팅되어 반환
- Agent의 결과를 향후 평가 하기 위해 구조를 정의
- 모델에 따라 사용되는 방식 상이함(클로드 5 버전부터는 랭체인의 구조화된 api 사용 제한)
    - 응답 결과를 LLM이 조정하는 절차를 거쳐서 처리

# 구조
```
/
L steps
    L step16_structured_output.py : 테스트용
L app
    L output.py : 출력 형식에 관련된 form 구성, pydantic 활용
    L agent
        L graph.py : output.py에서 만든 모델을 출력에 적용
```