import asyncio
from app.main import run

query = "상품 자체 하자의 환불 조건을 근거와 함께 알려줘."

asyncio.run(
    run(query)
)