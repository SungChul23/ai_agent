# 목표
- MCP 이해, 직접 구성, 연동, tool로 사용
    - Model Context `Protocol`
    - `LLM/Agent`와 `외부` 도구/데이터/서비스를 연결하기 위한 `표준 통신 규격`
    - github 공식 MCP
        - https://github.com/github/github-mcp-server
    - 그외 오피셜 MCP 
        - 국내
            - https://playmcp.kakao.com/
            - ..
        - 해외
            - ..
        - 서비스 주체별 MCP 제공
    - 사용
        - 이미 구성된 MCP 사용 -> 서비스 업체(노션, 슬렉등에서 개방된 규격 사용하면 본인 앱에서 연동가능)
        - playmcp등 해당 사이트는 사용의 제한(클로드,openai등 특정 회사를 거쳐서 사용 가능함)

    - 장점
        - Agent <->  MCP 표준화   <-> 서비스등
            - 누가 만들어도 MCP 규격을 준수하면 어떤 LLM/Agent도 호환 가능하게 됨
        - 각 서비스 주체들은 오피셜 MCP 개발하여 개방해줌
            - 서비스명 + MCP => 확인 or MCP 커뮤니티/공인(포털) 사이트 검색 사용 => 바로 적용됨
        - 사내용 MCP 없음 => 비공개용, 사내용임 

- 참고
    - MCP 구성 요소
    
        | 구성 | 역할 | 현재 예제 |
        |---|---|---|
        | **MCP Host** | MCP를 사용하는 전체 애플리케이션 | LangChain Agent |
        | **MCP Client** | MCP Server와 통신 | `FastMCP Client` |
        | **MCP Server** | Tool을 외부에 제공 | `exchange_server.py` |

    - MCP Server를 개발하여 24시간 운영되는 어딘가의 호스팅/클라우드등에서 운영
        - 운영/관리 비용 발생
        - playmcp, 기타 밴더들에서 운영하는곳에 등록 해당 비용 상쇄할수 있음
    - MCP Server와 통신하여서 해당 서비스를 이용하기 위해서는 MCP Client를 개발해야함
        - FastMCP 패키지를 이용하여 개발
    - 개발자가 만드는 AI 서비스에서 MCP를 사용한다면, MCP Client가 개발/설치되어서 사용되어야함
        - LLM/Agent가 도구로서 MCP Client을 사용 -> MCP Server로 요청이 가고 -> 외부 서비스와 엑세스 요청/응답 -> 응답 -> LLM/Agent까지 도달함
        - 개발자가 만드는 AI 서비스 => MCP host 라고 부름


# 구조
```
/
L mcp_servers
    L exchange_server.py    : 편의상 MCP Server 역활, MCP host에 위치시킴
L app
    L tools
        L mcp_tools.py      : MCP Client 역활, 랭그래프상 도구로 등록 -> Agent에서 사용
L steps
    L step15_mcp.py         : MCP 테스트용,  MCP host 포지션
```