'''
- 랭그래프 구성시 노드들이 등록됨
- 노드 사이에 공유할 Agent 상태 스키마 제공
- 메세지, tool 반복 사용횟수, 최종 구조화 응답 상태등등 관리
'''

# MessagesState 를 상속받은 클레스는 랭그래프의 상태관리용 사용가능함
from langgraph.graph import MessagesState
from app.output import AgentResponse

class AgentState(MessagesState):
    # 라운드라는 정보만 일단 구성
    rounds: int
    # 최종 구조화된 응답
    final:AgentResponse|None
    # 하네스용 추가
    tool_rounds: int  # 툴 실행 라운드 횟수
    start_at:float    # 수행 시간 측정 시작 시간 세팅