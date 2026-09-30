'''
- Agent가 rag 기능을 사용하기 위해서 툴로 등록 내용
'''

from langchain_core.tools import tool
from app.retrieval import advanced_search

# 툴로 구성, 등록 절차
# @tool를 함수의 데코레이터 자리에 배치
@tool
def search_company_policy(query: str, department: str = "") -> str:
    '''
        사내 HR/CS/SALES 규정과 정책을 검색한다. 해당 내용은 LLM 한번도 접하지 못한 내용인 사내 정보
        부서를 알고나 추정할 있다면 HR, CS, SALES들 중 하나를 검색시 반영하면 된다.    
    '''
    rows = advanced_search(query, department=department or None, k=5) # k 값은 에이전트 선택 못하게 고정(변동가능)
    if not rows: return "사내 규정 없음"
    # "\n\n" : 문단 구분값
    # [source=CS-REFUND-2026 | hybrid=0.389] 일반 반품은 상품 수령 ....
    # [source=CS-REFUND-2026 | hybrid=0.289] bbb ....
    # [source=CS-REFUND-2026 | hybrid=0.189] aa ....
    # [source=CS-REFUND-2026 | hybrid=0.089] ccc ....
    # [source=CS-REFUND-2026 | hybrid=0.009] ppp ....
    # 우의 문단들을 하나의 말뭉치로 구성하여 LLM에 추론시 근거 자료로 제공
    return "\n\n".join( f"[source={row[0]} | hybrid={row[-1]:.3f}]\n{row[4]}" for row in rows )