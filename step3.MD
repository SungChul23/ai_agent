# 목표
- 프럼프트 엔지니어링 적용
```
# Role(역활)

# Context(내용)

# Task(실제로 할일, 지시사항)

# Constraints(제약)
```
- 필요시 퓨샷(샘플 제공) 적용
- 프럼프트의 양식(폼, 형태)는 최적의 답을 얻기 위한 애플리케이션의 핵심 내용 관리
    - 서비싀 핵심 자산 관리해야함

# 구조
```
/
L app/
    L prompts.py  : 프럼프트 구성, 퓨샷
L stpes/
    L step3_prompt_engineering.py : 프럼프트 엔지니어링 기술 적용하여 LLM 질의

```

# 프롬포트 출력
```
당신은 B2B SaaS 전문 마케터입니다.

# Context
제품: AI 고객 상담 솔루션
대상: 온라인 쇼핑물 CS팀

# Task
핵심 가치를 설명하는 홍보 문구를 작성하세요.

# Constraints
- 5줄 이내
- 과장된 수치 금지
- 마지막에 CTA 1문장

```

# 실행 결과
```
stopReason : end_turn
usage      : {'inputTokens': 147, 'outputTokens': 174, 'totalTokens': 321, 'cacheReadInputTokens': 0, 'cacheWriteInputTokens': 0}
block types: ['text']
----------------------------------------
반복되는 문의에 CS팀의 시간을 쏟지 마세요.
AI가 자주 묻는 질문을 먼저 응대하고, 복잡한 상담만 팀원에게 연결합니다.
고객은 더 빠른 답변을, CS팀은 더 여유로운 하루를 얻습니다.
쇼핑몰 운영 환경에 맞춰 유연하게 적용할 수 있습니다.

지금 바로 무료 데모를 신청해 보세요.
```