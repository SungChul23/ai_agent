'''
- MCP Client 담당
- MCP Server과 통신 담당
- 랭그래프에 툴노드에 등록 됨
- Agent가 필요하면 도구로 사용
'''

# 1. 모듈 가져오기
from pathlib import Path
from fastmcp import Client
from langchain_core.tools import tool

# 2. MCP 서버가 백엔드등에서 구동되어 있지 않으므로, 직접 경로를 접근하여 실행
#    경로 획득
ROOT = Path(__file__).resolve().parents[2] # 프로젝트 루트까지 Path 경로 획득
#    실제 MCP Server 경로
SERVER = ROOT / "mcp_servers" / "exchange_server.py"

# 3. Tool 구성
@tool
async def get_exchange_rate(base: str="USD", quote: str="KRW" ) -> str:
    '''
        MCP 서버에서 환율 정보를 조회한다. 단, 실시간 환율은 아님.
        USD, EUR, JPY 대비 KRW에 대한 환율 정보만 지원한다.
    '''
    # MCP Server에 MCP Client 연결
    async with Client(SERVER) as client:
        print( "MCP 서버 연결 완료")

        # MCP 서버의 tool 호출
        result = await client.call_tool(
            name      ="get_exchange_rate",
            arguments = {
                "base" : base,
                "quote": quote
            }
        )

        # 실행 결과 문자열 변환, 아웃풋 포멧 심플하게 구성(컨셉)
        return str(result.data)