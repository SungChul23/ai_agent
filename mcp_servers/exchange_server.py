'''
- 당일 환율 요청하면 응답
- 원래 구성이라면, 환율 API 제공해주는 업체와 연동하여서 MCP Client 요청시 응답하는 구조로
  특정 클라우드등 서버에 위치한다
'''
# 1. 모듈 가져오기
from fastmcp import FastMCP

# 2. FastMCP 생성
mcp = FastMCP("exchange-mcp")

# 3. LLM이 호출시 응답할 MCP TOOL 구성
@mcp.tool
def get_exchange_rate(base: str="USD", quote: str="KRW" ) -> dict:
    '''
        임시용. 고정값으로 응답 (실시간 환율 정보 x)
    '''
    # 실제 외부 서비스와 통신하여 처리되는 부분을 더미로 구성
    # 환율 데이터
    rates = {
        ("USE","KRW"):1364.30,
        ("EUR","KRW"):1533.61,
        ("JPY","KRW"):863.24
    }
    # 키 구성
    key = (base.upper(), quote.upper())

    # 미지원 통화 예외처리
    if key not in rates:
        raise ValueError("미지원 통화")

    # TOOL의 결과 반환
    return {
        "base" : key[0],
        "quote": key[1],
        "rate" : rates[key],
        # --- 필요한 정보 삽입
        "meta" : "dummy-exchange-rate"
    }

# 직접 더미 실행
if __name__ == '__main__':
    mcp.run()