# 목표
- LangGraph + bedrock + LangChain + tools 
- LangGraph
    - StateGraph -> Agent -> ToolNode -> Agent 순환루프를 구성하는 자율형 에이전트 기본 구성
    - Reason/Tool/Observe 루프 구성
- 질의 -> 적절한 Tool을 LLM이 선택하고, Tool 사용, 결과를 이용하여 관찰 -> 최종 답변까지 반복 진행 체크
- 랭그래프 관점에서
    - 노드 : ToolNode, AgentNode등 존재
    - 순서, 방향성 지정
        - 시작점 지정
        - A노드에서 반드시 B노드로 간다
        - 끝점 지정
    - 끝 노드의 출력값 -> 최종 추론 결과
    - 노드를 순환하면서 다양한 노드사용 -> 흔적이 남음 -> MessagesState를 상속받은 객체에 저장
        - MessagesState는 messages(list) 변수에 순서대로 기록함
        - 통상 MessagesState를 상속받아서 커스텀 변수를 추가하여 노드상 State 관리 수행

# 구조
```
/
L app
    L agent
        L __init__.py
        L graph.py      : 랭그래프 구성 (노드 추가하는등 구성)
        L prompts.py    : 에이전트의 프럼프트
        L state.py      : 상태관리
    L main.py           : 에이전트 구동
L steps
    L step12_langgraph_agent.py : 테스트 코드
```

# 실행
```
python -m steps.step12_langgraph_agent
---

- query = "상품 하자로 반품할 경우 환불 기간과 배송비 부담 주체를 알려주세요"
---
HumanMessage -> AIMessage Tool use 판단 -> ToolMessage -> AIMessage END로 판단 -> 종료
[
    HumanMessage(content='상품 하자로 반품할 경우 환불 기간과 배송비 부담 주체를 알려주세요', additional_kwargs={}, response_metadata={}, id='bc667801-cb91-4a8d-a0d2-8b044f486419'), 
    
    AIMessage(content=[{'type': 'reasoning_content', 'reasoning_content': {'text': '', 'signature': 'ErkCCnkIEhABGAIqQE1BK+fQ6X4sKWQkN6rVDaZt6OisAXj3Wo8ZmJC6vOIMik1m+VPijMnTRns6iKEV7EB3lusxC/f4T+aTDpn3TKEyDmNsYXVkZS1zYWZmcm9uOABCCHRoaW5raW5nWgw4Mjc5MTM2MTc2MzWoAfjp9tUGEgyCA2lIwRV/YQeTg7caDEN8L6H+Al6iFsv/4CIwOxLdYMxcZkuHO1nSfWngegvu9Nf9IfLKp6ytdzuQlidh5wxkUrkyU5shZbK54s4YKm4r72R6uLUrVB3YHLsT/Fg4NNCAJIWI68cv0spc+j2IPh5rXehc8EdsqanmNZY2di7/hrlpNA0IcXBWgvDknbeEvdBTAbPdt5We5MJxRVANpny5Yl1pfwLWuN+5CzxPpBUtlrXTYWFLCnleHwp/IRgB'}}, {'type': 'tool_use', 'name': 'search_company_policy', 'input': {'query': '상품 하자 반품 환불 기간 및 배송비 부담 주체', 'department': 'CS'}, 'id': 'tooluse_liKqIuda0AIbqghLqHnLv0'}], additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': 'c2820eba-d7e7-4b55-be4a-8e7e4e1cc068', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 01 Oct 2026 01:18:48 GMT', 'content-type': 'application/json', 'content-length': '1005', 'connection': 'keep-alive', 'x-amzn-requestid': 'c2820eba-d7e7-4b55-be4a-8e7e4e1cc068'}, 'RetryAttempts': 0}, 'stopReason': 'tool_use', 'metrics': {'latencyMs': [3321]}, 'model_provider': 'bedrock_converse', 'model_name': 'us.anthropic.claude-sonnet-5'}, id='lc_run--01a0f50b-404c-7fd1-82d1-fde91e6fdf5c-0', tool_calls=[{'name': 'search_company_policy', 'args': {'query': '상품 하자 반품 환불 기간 및 배송비 부담 주체', 'department': 'CS'}, 'id': 'tooluse_liKqIuda0AIbqghLqHnLv0', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1081, 'output_tokens': 125, 'total_tokens': 1206, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}), 
    
    ToolMessage(content='[source=CS-REFUND-2026 | hybrid=0.322]\n# 고객 반품 및 환불 정책\n\n[source=CS-REFUND-2026 | hybrid=0.290]\n상품 자체의 제조상 하자나 기능상 문제가 확인되면 상품 수령 후 30일 이내 교환 또는 환불을 신청할 수 있다. 이 경우 고객에게 귀책사유가 없는 것으로 판단되면 회수 배송비와 교환 상품의 재배송 비용은 회사가 부담한다. 필요한 경우 고객센터는 사진, 동영상 또는 제품 상태 확인 자료를 요청할 수 있다.\n\n[source=CS-REFUND-2026 | hybrid=0.264]\n환불은 반품 상품이 물류센터에 도착하여 검수된 이후 진행한다. 검수 과정에서는 상품의 사용 여부, 구성품 누락 여부, 훼손 여부와 반품 사유를 확인한다. 정상 반품으로 확인된 경우 원결제 수단을 기준으로 환불하며, 카드사나 결제대행사의 처리 일정에 따라 실제 환불 완료 시점에는 차이가 발생할 수 있다.\n\n[source=CS-REFUND-2026 | hybrid=0.263]\n일반 반품은 상품 수령 후 7일 이내 신청할 수 있다. 고객은 주문번호와 반품 사유를 고객센터 또는 온라인 반품 신청 화면을 통해 접수해야 한다. 단순 변심에 의한 반품은 상품이 사용되지 않았고 포장 및 구성품이 정상적으로 보존된 경우에 한해 처리한다.\n\n[source=CS-REFUND-2026 | hybrid=0.242]\n단순 변심에 의한 반품의 왕복 배송비는 원칙적으로 고객이 부담한다. 무료배송 주문을 전체 반품하는 경우 최초 배송비를 포함한 왕복 배송비가 환불금에서 차감될 수 있다. 일부 상품만 반품하는 경우에는 반품 이후의 주문 금액이 무료배송 기준을 충족하는지에 따라 최초 배송비가 추가로 부과될 수 있다.', name='search_company_policy', id='919f6818-d335-413a-9c32-a89b1fc2efde', tool_call_id='tooluse_liKqIuda0AIbqghLqHnLv0'), 
    
    
    AIMessage(content='## 상품 하자 반품 정책 (문서: CS-REFUND-2026)\n\n**1. 환불 신청 기간**\n- 상품 수령 후 **30일 이내**에 교환 또는 환불 신청 가능 (단순 변심 반품의 7일보다 긴 기간 적용)\n\n**2. 배송비 부담 주체**\n- 상품 자체의 **제조상 하자나 기능상 문제**로 인한 반품의 경우, 고객 귀책사유가 없다고 판단되면:\n  - 회수 배송비: **회사 부담**\n  - 교환 상품 재배송비: **회사 부담**\n\n**3. 추가 절차**\n- 고객센터에서 하자 확인을 위해 **사진, 동영상, 제품 상태 확인 자료**를 요청할 수 있음\n- 환불은 반품 상품이 물류센터에 도착하여 **검수 완료된 이후** 진행됨\n- 검수 시 상품 사용 여부, 구성품 누락, 훼손 여부, 반품 사유 등을 확인\n- 정상 반품 확인 시 **원결제 수단 기준**으로 환불 처리 (카드사/결제대행사 처리 일정에 따라 실제 환불 완료 시점은 차이 발생 가능)\n\n> 참고로 단순 변심에 의한 반품은 7일 이내 신청, 왕복 배송비는 원칙적으로 고객 부담이라는 점에서 하자 반품과 차이가 있습니다.', additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': '34145237-ce19-4c74-a87f-78713edd9c15', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 01 Oct 2026 01:18:57 GMT', 'content-type': 'application/json', 'content-length': '1495', 'connection': 'keep-alive', 'x-amzn-requestid': '34145237-ce19-4c74-a87f-78713edd9c15'}, 'RetryAttempts': 0}, 'stopReason': 'end_turn', 'metrics': {'latencyMs': [7190]}, 'model_provider': 'bedrock_converse', 'model_name': 'us.anthropic.claude-sonnet-5'}, id='lc_run--01a0f50b-554f-7d33-9824-47f4286aef28-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 2003, 'output_tokens': 520, 'total_tokens': 2523, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}})]
++++++++++++++++++++++++++++++
[최종답변]

 ## 상품 하자 반품 정책 (문서: CS-REFUND-2026)

**1. 환불 신청 기간**
- 상품 수령 후 **30일 이내**에 교환 또는 환불 신청 가능 (단순 변심 반품의 7일보다 긴 기간 적용)

**2. 배송비 부담 주체**
- 상품 자체의 **제조상 하자나 기능상 문제**로 인한 반품의 경우, 고객 귀책사유가 없다고 판단되면:
  - 회수 배송비: **회사 부담**
  - 교환 상품 재배송비: **회사 부담**

**3. 추가 절차**
- 고객센터에서 하자 확인을 위해 **사진, 동영상, 제품 상태 확인 자료**를 요청할 수 있음
- 환불은 반품 상품이 물류센터에 도착하여 **검수 완료된 이후** 진행됨
- 검수 시 상품 사용 여부, 구성품 누락, 훼손 여부, 반품 사유 등을 확인
- 정상 반품 확인 시 **원결제 수단 기준**으로 환불 처리 (카드사/결제대행사 처리 일정에 따라 실제 환불 완료 시점은 차이 발생 가능)

> 참고로 단순 변심에 의한 반품은 7일 이내 신청, 왕복 배송비는 원칙적으로 고객 부담이라는 점에서 하자 반품과 차이가 있습니다.
++++++++++++++++++++++++++++++
```

# 판단 흐름
```
result["messages"]

[0] HumanMessage
    └─ 사용자 질문

[1] AIMessage
    └─ Tool Calls
        ├─ sales_summary
        └─ top_products

[2] ToolMessage
    └─ sales_summary 결과
    └─ top_products 결과

[3] AIMessage
    └─ 최종 답변

rounds = 2 (LLM 두번 추론)
```


# 요구사항 분석 2
- query = "2026-09-01부터 2026-09-05까지 매출과 상위 3개 상품을 알려줘"
```
[
    HumanMessage(content='2026-09-01부터 2026-09-05까지 매출과 상위 3개 상품을 알려줘', additional_kwargs={}, response_metadata={}, id='05567742-c942-4539-ba83-7065fd168782'), \
    
    AIMessage(content=[{'type': 'tool_use', 'name': 'sales_summary', 'input': {'start_date': '2026-09-01', 'end_date': '2026-09-05'}, 'id': 'tooluse_TR5AJWW2njwIehlFfHTd6i'}, {'type': 'tool_use', 'name': 'top_products', 'input': {'start_date': '2026-09-01', 'end_date': '2026-09-05', 'limit': 3}, 'id': 'tooluse_6if8uz6zioJuHulQv9zbl2'}], additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': '46999fcd-5c81-4985-90f0-64257d9c059a', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 01 Oct 2026 01:27:43 GMT', 'content-type': 'application/json', 'content-length': '635', 'connection': 'keep-alive', 'x-amzn-requestid': '46999fcd-5c81-4985-90f0-64257d9c059a'}, 'RetryAttempts': 0}, 'stopReason': 'tool_use', 'metrics': {'latencyMs': [2721]}, 'model_provider': 'bedrock_converse', 'model_name': 'us.anthropic.claude-sonnet-5'}, id='lc_run--01a0f513-6be9-7001-a57d-4d5796b1b0d3-0', tool_calls=[{'name': 'sales_summary', 'args': {'start_date': '2026-09-01', 'end_date': '2026-09-05'}, 'id': 'tooluse_TR5AJWW2njwIehlFfHTd6i', 'type': 'tool_call'}, {'name': 'top_products', 'args': {'start_date': '2026-09-01', 'end_date': '2026-09-05', 'limit': 3}, 'id': 'tooluse_6if8uz6zioJuHulQv9zbl2', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1080, 'output_tokens': 185, 'total_tokens': 1265, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}}), 
    
    ToolMessage(content='revenue=3586000.00, orders=8, range=2026-09-01~2026-09-05', name='sales_summary', id='c1f53554-0c8f-4ea9-8aec-9536e66ba015', tool_call_id='tooluse_TR5AJWW2njwIehlFfHTd6i'), 
    
    ToolMessage(content='1. 사내 AI Agent 구축: qty=1, revenue=1200000.00\n2. RAG 구축 컨설팅: qty=1, revenue=800000.00\n3. 데이터 분석 패키지: qty=4, revenue=600000.00', name='top_products', id='c162c63e-fea9-4742-aa27-0e8faa49bc5a', tool_call_id='tooluse_6if8uz6zioJuHulQv9zbl2'), 
    
    AIMessage(content='## 2026-09-01 ~ 2026-09-05 매출 요약\n\n**전체 매출 집계** (결제 완료 기준)\n- 총 매출: **3,586,000원**\n- 총 주문 건수: **8건**\n\n**상위 3개 상품** (매출 기준)\n\n| 순위 | 제품명 | 판매 수량 | 매출액 |\n|---|---|---|---|\n| 1 | 사내 AI Agent 구축 | 1 | 1,200,000원 |\n| 2 | RAG 구축 컨설팅 | 1 | 800,000원 |\n| 3 | 데이터 분석 패키지 | 4 | 600,000원 |\n\n추가로 특정 상품의 상세 트렌드나 다른 기간과의 비교가 필요하시면 말씀해 주세요.', additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': '63f76402-4aa0-4636-b0a0-37941a70a309', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 01 Oct 2026 01:27:48 GMT', 'content-type': 'application/json', 'content-length': '855', 'connection': 'keep-alive', 'x-amzn-requestid': '63f76402-4aa0-4636-b0a0-37941a70a309'}, 'RetryAttempts': 0}, 'stopReason': 'end_turn', 'metrics': {'latencyMs': [4273]}, 'model_provider': 'bedrock_converse', 'model_name': 'us.anthropic.claude-sonnet-5'}, id='lc_run--01a0f513-7957-7cf2-ba5e-1ad5581972b8-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 1439, 'output_tokens': 276, 'total_tokens': 1715, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}})]
```