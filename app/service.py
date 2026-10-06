'''
fastapi 기반 에이전트 서비스
'''
# 1. 모듈 가져오기
from fastapi import FastAPI
from pydantic import BaseModel
from app.main import invoke_agent

# 2. FastAPI 객체 생성
app = FastAPI(title="에이전트 서비스", description="랭그래프+bedrock+Agent", version="1.0.0")

# 3. 요청시 데이터 구조
class ChatRequest(BaseModel):
    message:str

# 4. 라우팅
# 4-1. /chat
@app.post("/chat")
async def chat(req:ChatRequest):
    # 1. 에이전트 질문 담아서 요청
    result = await invoke_agent(req.message)
    # 2. 응답 결과중 구조화된 데이터 획득
    final  = result.get('final')
    print( req.message, " => ", final )
    # 아웃풋 포멧팅 완료되면
    if final:
        return final.model_dump() # 객체 직렬화
    # 3. 응답 메세지 구성
    return {
        "answer"     : result['messages'][-1].content,
        "sources"    : [],
        "tools_used" : [],
        "confidence" : 0.0
    }
    pass

# 4-2. /health
# 서버가 잘 운용중인지, 살아있는지 점검용. bat로 인프라 구성시 중간에 활용됨, 인프라 구성후 outputs.tf에서 사용
@app.get("/health")
async def health():
    return {"status":"ok"}