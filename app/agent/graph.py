'''
- 랭그래프 구성
- Agent 구성
- 랭그래프에 agent, tools등을 등록, 순서 지정, 사용가능한 형태로 빌드
'''

# 1. 필요 모듈 획득
from langchain_core.messages import SystemMessage  # Agent 구성시 프럼프트에 System 프럼프트용
from langgraph.graph import StateGraph, START, END # 랭그래프의 구성 요소
from langgraph.prebuilt import ToolNode, tools_condition # Tool 실행, 호출여부 판단
from app.llm import get_chat_model # LLM 모델
from app.agent.state import AgentState # 랭그래프상에서 상태관리용
from app.agent.prompts import SYSTEM_PROMPT
from app.tools.sql_tools import sales_summary, top_products, refund_summary  # SQL Tool
from app.tools.rag_tools import search_company_policy # rag tool
from app.tools.memory_tools import remember_user_preference, recall_user_memory # 메모리 툴
from app.tools.mcp_tools import get_exchange_rate # MCP 도구

# 최종 응답의 출력 형식 정의한 pydantic 모델
from app.output import AgentResponse

# 2. 툴 목록 구성
TOOLS = [sales_summary, top_products, refund_summary, search_company_policy, remember_user_preference, recall_user_memory, get_exchange_rate]

# 4. 노드 분기 함수
def route_after_agent(state:AgentState):
    # 툴 호출이 존재하면 툴 노드로 이동, 없다면 최종 출력 포멧(format)로 이동
    return "tools" if getattr(state['messages'][-1], "tool_calls", None) else "format"

# 3. 그래프 빌드
def build_graph():
    # 추론만 담당 LLM
    model = get_chat_model()
    # 도구를 사용하는 LLM, LLM에 Tool 연결
    bind_model = model.bind_tools( TOOLS )

    # Agent 노드 -> 추론만 할것인가? 도구를 사용하여 결과를 가지고 추론을 할것인가?
    async def call_model(state:AgentState):
        # 1. 라운드 값 획득 (랭그래프내에서 순환을 몇번했는가?, LLM 추론을 몇번 했는가?) # Agent 수행 횟수
        rounds = state.get('rounds', 0)
        # 2. 라운드를 기점으로 모델 선택
        #    차후, 모델을 여러 케이스로 준비(모델 id, 제품(gpt, claude, 도구등록 상이하게))
        select_model = model if rounds >=6 else bind_model # 6회 이상이면 그냥 추론, 이하면 도구를 이용한 추론
        # 3. 비동기 추론 호출
        response = await select_model.ainvoke(
            # 도구를 사용했다면, 첫번째가 아니라면 messages에 기록이 존재함 -> 그간 추론, 행동한 모든 내역을 같이 보냄
            [SystemMessage(content=SYSTEM_PROMPT), *state['messages']]
        )
        # 4. 추론결과, 라운드(LLM 1회 호출) + 1 하여 반환 -> state['messages']에 기록됨 => 상태관리
        return {"messages":[response], "rounds": rounds+1}

    # Agent 최종 답변을 JSON으로 구조화 하는 노드
    async def format_ouptut(state:AgentState):
        # claude 기준 모델 버전이 5로 진입한 이후 => 답변 구조화 랭체인 api 사용 x => LLM으로 처리하도록 변경

        # 구조화대한 LLM 호출
        response = await model.ainvoke()


    
    # 3-1. 그래프 생성
    graph = StateGraph( AgentState )            # 상태 정보를 가진 그래프 생성
    
    # 3-2. 노드 등록 (LLM 추론, 도구 )
    graph.add_node("agent", call_model)         # LLM Agent 노드 등록
    # handle_tool_errors : 툴 실행중에 에러 발생시 에이전트 전체를 바로 싪패시키지 않고 오류를 처리하여 agent 대응하게 할것인가?
    graph.add_node("tools", ToolNode(TOOLS, handle_tool_errors=True) )
    # 출력 포멧 처리
    graph.add_node("format", format_ouptut)

    # 3-3. 흐름 구성(실행방향 지정)
    # 시작점
    graph.add_edge(START, "agent")              # 시작->Agent 
    # 조건부 실행 (에이전트가 툴을 사용하겠다, 아니면 END 이동 -> 추론을 통해서 판단)
    '''
             tools_condition
                   │
          ┌────────┴────────┐
          ↓                 ↓
      "tools"              END       <- tools_condition 함수의 반환값
          │                 │
          ↓                 ↓
     tools 노드            END (종료) <- 이동할 노드
    '''
    graph.add_conditional_edges("agent", 
                                # 분기함수가 메세지 검사-> 툴 사용확인되면 툴노드이동, 아니면 포멧노드 이동
                                route_after_agent, 
                                {
                                    "tools":"tools", 
                                    "format":"format"
                                })
    # 툴 사용 이후 방향성
    graph.add_edge("tools","agent") # 툴 사용 => 에이전트 진행

    # 포멧노드 -> END
    graph.add_edge("format", END)
       
    
    # 3-4 그래프 컴파일및 반환 -> 실행 가능한 형태로 구성 반환
    return graph.compile()