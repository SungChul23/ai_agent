'''
MCP Host 역활, 실제 만들고자 하는 앱/서비스
'''
import asyncio
from app.main import run

async def demo():
    await run("달러 대비 원화 환율을 확인해.")

    await run("위완화 대비 원화 환율을 확인해.")

asyncio.run( demo() )