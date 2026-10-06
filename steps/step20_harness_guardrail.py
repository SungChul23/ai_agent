'''
- 하네스를 적용하여 에이전트 작동시키는 테스트 코드
'''
# 기능 확인
from app.harness import ALLOWED_TOOLS, Budget, assert_allowed_tool

# # 버짓 생성
# b = Budget()
# b.consume_tool_round()
# print("라운드, 시간 체크 객체")

import asyncio
from app.main import run

async def main():    
    result = await run("2026년 9월 매출을 요약해줘.")
    final  = result.get('final')
    print( final.answer if final else result["messages"][-1].content)

asyncio.run(
   main()
)