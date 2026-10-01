# 목표
- Agent Memory
- PostgreSQL + pgvector 방식으로 지식 저장(현재) + Memory 저장소 활용
- Memory 저장소 활용하면 짧은 답변, 기존 질문의 대한 답변을 메모리에서 체크하여 LLM 사용 없이 응답 가능한 구조 구성 -> 중요도 관리 -> 토큰 비용(운영비) 절감 도움- 
- 장기기억 활용

- 역활
    - llm : 판단, 답변을 담당 두뇌
    - RAG : 회사 문서, 규정등 llm 모르는 정보
    - db  : 실제 데이터들 저장, 조회
    - MEMORY : 사용자의 맥락 기억, 패턴 기억 -> 사용자 주의, 답변형태, 업무 형태, 기억포인트등등 저장 -> 사용자 질문시 해당 내용을 기반으로 답변할때 제공
        - 사용자의 선호하는 방식으로 답변을 구성하게 도움
        - llm이 추론을 할대, 사용자가 누구고, 어떤 업무를 하고, 어떤 방식으로 답변 받기를 원하지는 삽입( 프럼프트)
        - llM이 사용자를 처음 만난 사람처럼 행동하지 말고, 과거의 중요한 정보(맥락)을 제공하는 역활 담당

# 구조
```
/
L sql
    L 005_memory.sql        : 사용자의 정보를 저장하는 테이블, 검색
L app
    L tools
        L memory_tools.py   : sql 역활 담당, 기능적으로 메모리 역활
    L agent
        L graph.py          : 툴 등록
L steps
    L step14_memory.py      : 메모리 테스트
```

# sql 반영
```
python -m scripts.migrate
---
\dt

# 테이블 구조 확인
\d agent_memories
```