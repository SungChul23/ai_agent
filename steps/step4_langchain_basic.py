'''

- 랭체인 적용
- 업무 프로세스를 체인으로 연결 후 작동
    - 프롬포트, LLM 호출
'''

from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_chat_model

# 체인을 구성할 요소 생성
# system/human으로 구성된 , 역할을 명시한 대화형 프롬포트 템플릿 생성

prompt = chat_template = ChatPromptTemplate.from_messages([
    ("system", "당신은 최신 트렌드에 민감한 AI 전문가 입니다., 핵심만 설명합니다."),
    ("human","{topic}을 예시 1개와 함께 설명해주세요."),
])

# 랭체인의 체인 구성, 단계별로 진행할 내용 연결 (앞단계의 출력은 뒷단계의 입력). LCEL 형태를 따름, Runnable 파이프라인
# ChatPromptTemplate | ChatBedrockConverse
chain = prompt | get_chat_model()

# 체인호출
res = chain.invoke( {"topic":"LangChain Runnable 파이프라인"} )

# 결과출력
print( res.content )