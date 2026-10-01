'''
랭그래프기반 에이전트 실행하는 코드
'''
import asyncio
from app.agent.graph import build_graph

async def run(query: str):
    '''
        사용자 질문 => 랭그래프기반 에이전트 전달
    '''
    result = await build_graph().ainvoke(
        {"messages": [{"user": query}], "rounds": 0},
        config = {"recursion_limit": 18} # 재귀호출 제한 -> 무한루프 방지
    )

    print("최종 결과 : ", result["messages"])