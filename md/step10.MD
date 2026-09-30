'''
시멘틱 청킹을 이용한 하이브리드 검색
- 원문 문서 -> 시멘틱 청킹 처리
- 하이브리드 검색
'''
# 시멘틱 청킹
from app.ingestion.splitter import semantic_split_text, splite_text

# 임시 문서 (말뭉치 직접 제공) 사용 -> 차후 실제 문서도 대체
# 의도적으로 서로 다른 주제로 데모 문서 제공 (cs->hr->sales)
DEMO_TEXT = """
상품을 수령한 뒤 단순 변심으로 반품하려는 고객은 수령일로부터 7일 이내에 신청해야 합니다.
반품 상품은 사용 흔적이 없어야 하며 포장 상태가 보존되어야 합니다.
상품 자체의 하자가 확인되면 회사가 회수 배송비를 부담합니다.

연차 휴가는 근로자의 재충전을 위한 휴가 제도입니다.
직원은 사내 절차에 따라 희망 휴가일을 신청하고 승인 상태를 확인해야 합니다.
부서 일정과 업무 인수인계를 고려해 연차 사용 계획을 수립합니다.

월 매출 분석에서는 주문 금액, 판매 수량, 환불 금액을 함께 확인합니다.
전월 대비 증감률과 상품별 매출 비중을 계산하면 주요 매출 변화 원인을 찾을 수 있습니다.
""".strip()

# 1. 고정 크기 청킹 (문단 기준 청킹) (데모 텍스트가 작아서 chars수도 작게 임의 구성)
# paragraph_chunks = splite_text(DEMO_TEXT, max_chars=300)
# for i, chunk in enumerate( paragraph_chunks, 1):
#     print( f"[{i}] {chunk}")

# 문단 기준 청킹의 문제점 -> cs와 hr이 같은 맥락으로 청킹이 되었음 => 크기 기준으로 진행하다 보니 생기는 문제
# => 원소스 문서를 분리하면(각각 문서로 존재하면) 해결은 가능함
'''
[1] 상품을 수령한 뒤 단순 변심으로 반품하려는 고객은 수령일로부터 7일 이내에 신청해야 합니다.
반품 상품은 사용 흔적이 없어야 하며 포장 상태가 보존되어야 합니다.
상품 자체의 하자가 확인되면 회사가 회수 배송비를 부담합니다.

연차 휴가는 근로자의 재충전을 위한 휴가 제도입니다.
직원은 사내 절차에 따라 희망 휴가일을 신청하고 승인 상태를 확인해야 합니다.
부서 일정과 업무 인수인계를 고려해 연차 사용 계획을 수립합니다.
[2] 월 매출 분석에서는 주문 금액, 판매 수량, 환불 금액을 함께 확인합니다.
전월 대비 증감률과 상품별 매출 비중을 계산하면 주요 매출 변화 원인을 찾을 수 있습니다.
'''

# 2. 시멘틱 청킹 (데모 텍스트가 작아서 chars수도 작게 임의 구성)
# semantic_chunks  = semantic_split_text(DEMO_TEXT, threshold=0.55, max_chars=400)
# for i, chunk in enumerate( semantic_chunks, 1):
#     print( f"[{i}] {chunk}")


from app.retrieval import advanced_search
# 3. 검색
query = "상품 하자 환불 기간과 배송비 부담 주체"

# 하이브리드 검색

# 전체 청크 검색
# for row in advanced_search(query, k=5):
#     print( row[0], row[1], row[2], row[3], row[-2], row[-1], row[4][:20] )
#     print( row[4] )
#     break


# 대상 청크만 검색
# 필터를 활용 검색 -> CS만 검색등
# 정확한 필터링이면 빠른 응답 가능
# department가 틀리면 검색 결과가 부정확해짐 -> hr
for row in advanced_search(query, department="CS",  k=5):
    print( row[0], row[1], row[2], row[3], row[-2], row[-1], row[4][:20] )
    print( row[4] )
    break


# 이후 시나리오
# 검색 결과를 근거로 프럼프트에 넣어서 추론 => app.rag.answer() 참고