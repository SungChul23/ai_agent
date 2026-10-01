import asyncio
from app.main import run

query = "2026-09-01부터 2026-09-05까지 환불 현황을 확인하고, 상품 하자 환불 정책을 함계 설명해줘"

asyncio.run(
    run(query)
)