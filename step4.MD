# 목표
- 랭체인 이해, 간단한 체인 구성, LLM 호출
- 체인구성
    - 프롬포트 구성 -> LLM 호출
    - 해당 구성은 향후 복잡한 agent 구성으로 확장


# 구조

```
/
L app
    L llm.py : LLM에 대한 모듈
L step3
    L step4_langchain_basic.py : 체인구성 (prompt | LLM)

```

# 실행
```
 python -m steps.step4_langchain_basic
```

# 결과
```
    ## 개념
    **Runnable**은 LangChain의 모든 컴포넌트(프롬프트, LLM, 파서 등)가 공통으로 구현하는 인터페이스입니다. `|` (파이프) 연산자로 여러 컴포넌트를 체이닝할 수 있어 **LCEL(LangChain Expression Language)** 이라고 부릅니다.

    ## 핵심 장점
    - **일관된 인터페이스**: 모든 컴포넌트가 `invoke()`, `stream()`, `batch()` 지원
    - **직관적 연결**: `|`로 데이터 흐름을 명확하게 표현
    - **자동 최적화**: 병렬 처리, 스트리밍, 비동기 처리 자동 지원

    ---

    ## 예시 코드

    ```python
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    # 1. 컴포넌트 정의
    prompt = ChatPromptTemplate.from_template(
        "{topic}에 대해 한 줄로 설명해줘."
    )
    model = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()

    # 2. Runnable 파이프라인 구성 (LCEL)
    chain = prompt | model | parser

    # 3. 실행
    result = chain.invoke({"topic": "LangChain"})
    print(result)
    ```

    **출력 예시:**
    ```
    LangChain은 LLM 애플리케이션 개발을 위한 오픈소스 프레임워크입니다.
    ```

    ---

    ## 데이터 흐름
    ```
    {"topic": "LangChain"}
        ↓
    [prompt] → ChatPromptValue 생성
        ↓
    [model] → LLM이 응답 생성 (AIMessage)
        ↓
    [parser] → 문자열로 변환
        ↓
    최종 결과 (str)
    ```

    ## 추가 활용
    ```python
    # 스트리밍
    for chunk in chain.stream({"topic": "AI"}):
        print(chunk, end="", flush=True)

    # 배치 처리
    chain.batch([{"topic": "AI"}, {"topic": "ML"}])
    ```

    이처럼 `|` 연산자만으로 **파이프라인 조합 → 실행/스트리밍/배치**까지 일관되게 처리할 수 있는 것이 Runnable의 핵심입니다.

```