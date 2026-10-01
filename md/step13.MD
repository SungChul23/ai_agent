# 목표
- 랭그래프 + 정형데이터(postgresql) + 비정형 데이터(pgvector) 같이 추론의 지식(배경)으로 사용
- 환불 통계 (SQL tool)와 환불 정책 (Rag Tool)을 한 질문에서 함께 처리/사용

# sql
- 환불 통계을 위한 sql 처리
```
python -m scripts.migrate
---
select * from refunds;
 refund_id | order_id |      requested_at      |     reason     |  amount  |  status  
-----------+----------+------------------------+----------------+----------+----------
         1 |        8 | 2026-09-04 09:00:00+00 | product_defect | 99000.00 | approved
(1 row)

```

# 구조
```
/
L app
    L agent
        L graph.py            : refund_summary 도구 추가
    L tools
        L sql_tools.py        : 추가로 특정 날짜내에 환불 요청 건수, 금액, 사유등 조회
L steps
    L step13_sql_rag_agent.py : 질문을 가지고 llm 추론 진행
```

# 실행
```
python -m steps.step13_sql_rag_agent
---
=> 도구가 현재 제공되어 있지 않습니다. 특정 미션 해결 x
[최종답변]

 ## 1. 2026-09-01 ~ 2026-09-05 환불 현황

먼저 안내드릴 점은, 현재 제공된 도구는 다음과 같습니다.
- `sales_summary`: 결제 완료 매출/주문 건수 집계
- `top_products`: 결제 완료 매출 기준 상위 제품
- `search_company_policy`: 사내 정책 검색

**환불 건수, 환불 금액, 환불율 등을 직접 조회할 수 있는 도구가 현재 제공되어 있지 않습니다.** 매출 집계 도구(`sales_summary`)는 "결제 완료" 기준이며 환불/취소 데이터를 포함하지 않으므로, 이 데이터를 근거로 환불 현황을 추정하거나 생성해서 말씀드릴 수는 없습니다(사실 확인 불가 항목을 임의로 만들 수 없음).

➡️ 해당 기간의 환불 현황(건수/금액)을 정확히 알려드리려면 **환불 데이터 조회 도구**가 추가로 필요합니다. 필요하시면 환불 전용 조회 기능 연결 여부를 확인해 주시거나, 담당 CS팀에 직접 데이터를 요청하시는 것을 권장드립니다.

...
```