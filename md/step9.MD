# 목표
- RAG(Retrieval-Augmented Generation)
    - 검색 증강, LLM이 학습하지 않는 LLM 기준 외부 데이터( 사용자 관점 사내데이터등)를 검색(일치되는 정확한 정보)을 통해서 정보를 제공받아서 여기에 기존 프럼프트와 결합하여 LLM에게 추론 처리
    - 검색은 백터를 기반으로 진행 => 데이터는 백터화 되어 백터디비에 저장되어 있어야함
    - LLM이 답변하기 전에 외부 지식에서 필요한 정보를 검색(Retrieval)하고, 그 정보를 근거로 답변(Generation)하게 하는 방식
- Agent의 관점에서는 RAG는 Tool임
    - 도구를 사용하는 여부는
        - 규칙적 구성
        - 자율적 판단하게 구성
            - 정책 부여 : 사내 규정, 업무 지식등에 질문은 rag를 사용하라라는등 

- rag 기본 사용

# 구조
```
/
L app
    L retrieval.py       : 백터 디비에 검색 (질문 전달, k개)후 결과 반환 함수 제공
    L rag.py             : 질문 => 백터 디비 검색 => 결과+프럼프트 => LLM 추론요청 => 응답
L steps
    L step9_rag_basic.py : 검색 증강 테스트용
```

# 실행
```
python -m steps.step9_rag_basic
```