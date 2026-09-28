# 목표
- Amazone Bedrock을 이용하여 LLM을 직접호출

```
AWS 인증 -> Bedrock Runtime Client 생성 -> LLM에게 프롬포트 전달 -> 응답 파싱 (JSON)
```

# 구조
```
/
L app/              : 모듈 (타 프로젝트에서도 사용 가능하게 구조화)
    L bedrock.py    : Bedrock Runtime Client 생성
    L config.py     : 프로젝트 전체 환경변수 총괄 관리 (.env 로드, 추가)
L steps/
    L step2_bedrock_llm_call.py : Bedrock LLM 호출 테스트 
```

# 실행
```
python -m steps.step2_bedrock_llm_call

-----

# AI Agent 5줄 설명
1. **인식(Perception)**: 환경이나 사용자로부터 정보를 입력받아 상황을 인식합니다.
2. **판단(Reasoning)**: 입력된 정보를 바탕으로 목표 달성을 위해 어떤 행동이 필요한지 스스로 추론하고 계획합니다.
3. **행동(Action)**: 도구 사용, API 호출, 코드 실행 등 실제 작업을 자율적으로 수행합니다.
4. **기억(Memory)**: 이전 대화나 작업 결과를 기억하여 맥락을 유지하고 일관된 대응을 합니다.
5. **반복 개선(Iteration)**: 결과를 평가하고 필요시 계획을 수정하며, 최종 목표를 달성할 때까지 이 과정을 반복합니다.
**핵심**: 단순히 질문에 답하는 것을 넘어, 스스로 목표를 세우고 여러 단계를 거쳐 문제를 해결하는 자율적인 AI 시스템입니다.
```