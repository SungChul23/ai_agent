'''
- 랭그래프 구성
- Agent 구성
- 랭그래프에 agent, tools등을 등록, 순서 지정, 사용가능한 형태로 빌드
'''

# 1. 필요 모듈 획득
from langchain_core.messages import SystemMessage, HumanMessage  # Agent 구성시 프럼프트에 System 프럼프트용
from langgraph.graph import StateGraph, START, END # 랭그래프의 구성 요소
from langgraph.prebuilt import ToolNode, tools_condition # Tool 실행, 호출여부 판단
from app.llm import get_chat_model # LLM 모델
from app.agent.state import AgentState # 랭그래프상에서 상태관리용
from app.agent.prompts import SYSTEM_PROMPT
from app.tools.sql_tools import sales_summary, top_products, refund_summary  # SQL Tool
from app.tools.rag_tools import search_company_policy # rag tool
from app.tools.memory_tools import remember_user_preference, recall_user_memory # 메모리 툴
from app.tools.mcp_tools import get_exchange_rate # MCP 도구
# 하네스 도구 
from app.harness import ALLOWED_TOOLS, assert_allowed_tool, Budget

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
        # 최종 답변 획득
        answer = state['messages'][-1].content
        # 사용된 도구의 이름들
        tool_names = [
            getattr(m, "name","")
            for m in state['messages']
            if getattr(m, "type","")=='tool'
        ]

        # 구조화대한 LLM 호출
        response = await model.ainvoke([
            HumanMessage(content=f"""
                다음 답변을 JSON으로 구조화하세요.
                반드시 JSON만 출력하세요.

                형식:
                {{
                    "answer": "최종 답변",
                    "sources": ["근거 또는 출처"],
                    "tools_used": ["사용한 도구"],
                    "confidence": 0.0
                }}

                답변:
                {answer}

                실제 사용된 도구:
                {tool_names}

                규칙:
                - answer에는 최종 답변을 작성합니다.
                - sources에는 답변의 근거 또는 출처를 작성합니다.
                - tools_used에는 실제 사용된 도구만 작성합니다.
                - 근거가 없다면 sources는 빈 배열로 작성합니다.
                - confidence는 0.0~1.0 사이 숫자로 작성합니다.
                - 근거가 약하면 confidence를 낮추세요.
            """)
        ])

        # 응답 처리
        content = response.content.strip()
        # print( "+"*30 )
        # print( "구조화 요청 1차 결과값" )
        # print( content )
        # print( "+"*30 )
        # 앞뒤로 코드 삽입용 마크다운 삭제, 앞뒤 공백 제거
        '''
            구조화 요청 1차 결과값
            ```json
            {
                "answer": "## 상품 자체 하자 환불 조건 (근거: CS-REFUND-2026)\n\n**1. 신청 기한 및 조건**\n- 상품의 **제조상 하자**나 **기능상 문제**가 확인될 경우, **상품 수령 후 30일 이내**에 교환 또는 환불을 신청할 수 있습니다.\n\n**2. 비용 부담**\n- 고객에게 귀책사유가 없는 것으로 판단되면 **회수 배송비**와 **교환 상품 재배송 비용**을 회사가 부담합니다.\n\n**3. 증빙 자료**\n- 고객센터는 필요 시 **사진, 동영상, 제품 상태 확인 자료**를 요청할 수 있습니다.\n\n**4. 환불 처리 절차**\n- 환불은 반품 상품이 물류센터에 도착 후 **검수 완료 시점**부터진행됩니다.\n- 검수 시 사용 여부, 구성품 누락, 훼손 여부, 반품 사유를 확인하며, 정상 반품으로 확인되면 **원결제 수단 기준으로 환불**됩니다. (단, 카드사/PG사 처리 일정에 따라 실제 환불 완료 시점은 달라질 수 있음)\n\n**5. 부가 조건**\n- 사은품·증정품이 포함된 경우 함께반환해야 하며, 반환 불가 시 해당 금액이 환불금에서 차감될 수 있습니다.\n- 세트 상품은 특별한 안내가 없는 한 **전체 구성 기준**으로 반품 여부가 판단됩니다.\n\n※ 참고: 고객 과실로 인한 훼손·사용 흔적, 맞춤/각인 제작 상품은 **단순 변심 반품**과 관련된 제한 사항이며, 상품자체 하자의 경우에는 해당되지 않습니다.\n\n필요하시면 특정 기간의 실제 환불 건수·사유 통계도 함께 조회해드릴까요?",
                "sources": ["CS-REFUND-2026"],
                "tools_used": ["search_company_policy"],
                "confidence": 0.9
            }
            ```
        '''
        # 노이즈 제거
        content = content.removeprefix("```json").removesuffix("```").strip()
        # JSON문자열 => AgentResponse 객체로 세팅
        final_ar = AgentResponse.model_validate_json( content )

        # 상태객체에 final 키에 값을 부여한것임
        return {"final":final_ar}

    # 하네스 노드 구성
    async def check_harness(state:AgentState):
        # 1. 실행 회수 제한
        # 2. 해당 도구가 허락되었는지 체크 가능 -> 구성!!
        #    히스토리상, 마지막 메세지에서 툴사용(tool_calls) 표식이 있는지 체크, 있다면 값 획득
        tool_calls = getattr(state["messages"][-1], "tool_calls", [])
        for call in tool_calls:
            assert_allowed_tool( call['name'] )
            
        # 3. 수행시간? 이후
        pass
    
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