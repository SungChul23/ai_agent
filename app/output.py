'''
- 출력의 구조화를 위한 form 구성 (모델구성)
'''
from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    answer     : str       = Field(description="사용자에게 제공할 최종 답변")
    sources    : list[str] = Field(description="답변의 근거 또는 출처", default_factory=list)
    tools_used : list[str] = Field(description="실제 사용된 tool 목록", default_factory=list)
    confidence : float     = Field(description="답변 신뢰도", ge=0.0, le=1.0)