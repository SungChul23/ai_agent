'''
랭그래프기반 에이전트 실행하는 코드
'''
import asyncio
from app.agent.graph import build_graph

# 테스트용/Fastapi/slack등.. 공용
graph = build_graph()

# 에이전트 샐행 함수
async def invoke_agent(question:str):
    return await graph.ainvoke(
        {"messages":[("user", question)], "rounds":0, "final":None, "tool_rounds":0 },
        config = {"recursion_limit":18}
    )

async def run(query: str):
    '''
        사용자 질문 => 랭그래프기반 에이전트 전달
    '''
    result = await build_graph().ainvoke(
        # 사용자 메세지를 구성(상태내 messages키값으로), 라운드(llm 호출회수) 0으로 세팅 => AgentState 기본구성하여 호출
        {"messages":[("user", query)], "rounds":0, "final":None },
        # 전체 순환 회수 제한 (18회는 설정)
        config = {"recursion_limit":18}
    ) # 초기 상태를 설정하여 그래프에게 전달

    # 전체 맥락(상태의 변화들의 기록)
    # print( result )

    # 툴중심 상태 관리값 추출
    # for message in result["messages"]:
    #     if getattr(message, "tool_calls", None):
    #         print("TOOL CALLS  :", [ x.get('name') for x in message.tool_calls])
    #     if getattr(message, "type", ""):
    #         print("TOOL RESULT :", message.content)


    # 최종 답변 (LLM)
    print("+"*30)
    # #print("[최종답변]\n\n", result["messages"][-1].content )

    # # 출력 포멧을 설정한 이후 => final
    final = result.get('final')
    print("[최종답변]\n\n", final.model_dump_json(indent=2) if final else result["messages"][-1].content)
    print("+"*30)