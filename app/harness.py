'''
- 에이전트가 툴 사용시 제한 사항, 정책등 반영
'''

# 리소스 한도 => dataclass 테커레이터 사용
from dataclasses import dataclass
# 시간 한도
import time
# 툴 사용 한도 -> 툴 사용 목록 제한 -> 툴을 제한을 하면 -> 도구제한을 받음
ALLOWED_TOOLS = {"sales_summary", "top_products", "refund_summary", "search_company_policy", 
                 "remember_user_preference", "recall_user_memory", "get_exchange_rate"}

# 에이전트 실행시 허용할 한도 -> 값으로 세팅
@dataclass
class Limits:
    max_tool_rounds:int = 6     # 초대 tool 실행 라운드 횟수
    max_seconds:float = 120.0   # 최재 전체 실행 시간(초단위)
    # .... 필요한 제한값 추가

# 에이전트가 사전에 정한 한도를 넘지 않도록 관리
class Budget:
    # 생성자 : 맴버변수 초기화 진행(초기값 설정)
    def __init__(self,  
                 tool_rounds:int = 0,
                 start_at:float|None=None,
                 limits:Limits|None=None):
        # 인스턴스 맴버세팅
        self.limits  = limits or Limits()
        # 정확한 시간 측정을 위해서 프로그램에 영향을 받지 않는 함수 사용
        self.started = start_at or time.monotonic()
        # 툴 사용 라운드 관리
        self.tool_rounds = tool_rounds

    # Tool 실행 할때마다 횟수, 경과 시간 검사
    def consume_tool_round(self):
        # 툴사용 -> 라운드 1회 증가
        self.tool_rounds += 1
        # 체킹
        if self.tool_rounds > self.limits.max_tool_rounds:
            raise RuntimeError("툴 사용 제한 회수 초과")
        if time.monotonic() - self.started > self.limits.max_seconds:
            raise RuntimeError("실제 실행 시간 제한 초과.")

# 요청한 툴이 허용한 툴 목록에 존재하는가?
def assert_allowed_tool(name:str):
    # 에이전트별로 제한적으로 사용하도록 구성 가능 -> 에이전트, 툴이름 같이 받으면 -> 패턴구성
    if name not in ALLOWED_TOOLS:
        raise PermissionError(f"해당 툴 사용은 허락되지 않았다. {name}")