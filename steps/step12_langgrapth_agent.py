'''
사용자의 질문을 랭그래프에 전달하여 에이전트가 처리하도록 테스트
'''
import asyncio
from app.main import run

query = "상품 하자로 반품할 경우 환불 기간과 배송비 부담 주체를 알려주세요"

asyncio.run(
    run(query)
)