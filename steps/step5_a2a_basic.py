# 프럼프트
from langchain_core.prompts import ChatPromptTemplate
# llm 
from app.llm import get_chat_model
# 응답 결과 파싱
from langchain_core.output_parsers import StrOutputParser

# 신입 개발자 에이전트
developer_prompt = ChatPromptTemplate.from_messages([
  # 페르소나를 통해 신입 개발자 에이전트를 규정
  ("system", "당신은 열정적인 '신입 파이썬 개발자'입니다. 요청 받은 기능을 코드로 작성하세요. 설명은 최소화하고 코드 위주로 작성하세요."),  
  ("human", "{request}"),
])
# 체인구성
developer_agent = developer_prompt | get_chat_model() | StrOutputParser()


# 이전 에이전트의 출력이 다음 에이전트의 입력이 됨 
# 전문 리뷰어 에이전트
reviewer_prompt = ChatPromptTemplate.from_messages([
  ("system", "당신은 까다로운 '전문 개발자'입니다. 신입 개발자가 작성한 코드를 리뷰하세요. \n"
             "보안 취약성, 비효율적인 부분, 스타일 가이드를 점검하고 수정 제안을 하세요. \n"
             "코드가 완벽하다면 'PASS'라고만 답변하세요. \n"
   ),  
  ("human", "다음 코드를 리뷰해 주세요.\n\n{code}"),
])
# 체인구성 (고도화된 전문기능, 심도 있는 추론 => 모델 상위로 적용)
reviewer_agent = reviewer_prompt | get_chat_model() | StrOutputParser()

# 피드백 반영 에이전트
refinder_prompt = ChatPromptTemplate.from_messages([
  ("system", "당신은 열정적인 '신입 파이썬 개발자'입니다. 전문 개발자의 리뷰를 보고 코드를 수정해서 다시 제출하세요."),  
  ("human", "이전 코드:\n{orginal_code}\n\n, 리뷰 내용:\n{feedback}\n\n 위 내용을 반영하여 개선된 전체 코드를 다시 작성하세요."),
])
# 체인구성
refinder_agent = refinder_prompt | get_chat_model() | StrOutputParser()


def run_agent_collaboration( topic: str ) -> None:
    '''
        - 아주 간단한 에이전트(간단한 랭체인 구성)간 협업
        - 단방향 구조로 a2a 구성
    '''
    print(f'목표 {topic}\n' + '='*50)

    # round 1. 신입 개발자 초안 개발
    print("\n[신입 개발자] 코드 작성 중...") 
    draft_code = developer_agent.invoke( {"request": topic })
    print(f'---\n {draft_code[:200]} ... \n (코드 생략) \n ---')

    # round 2. 리뷰어가 피드백 제공 (평가)
    print("\n[전문 개발자] 코드 검토 중...") 
    feedback = reviewer_agent.invoke( {"code": draft_code })
    print(f'---\n {feedback} ... \n')

    # round 3. 평가 결과에 따라 분기 -> pass가 나오면 개발 종료, 아니면 피드백 반영
    if 'PASS' not in feedback: # 없다면
        print('\n[신입 개발자] 피드백 반영하여 수정 중...')
        final_code = refinder_agent.invoke({
            "orginal_code":draft_code,
            "feedback":feedback
        })
        # 순환 구조가 없기 때문에 단방향성 기준으로 여기서 마무리함 -> 랭그래프가 필요한 이유 (반복 가능, 에이전트 수 줄일수 있음)
        print('최종 결과물')
        print(final_code)
    else:
        print('최종 결과물')
        print(draft_code)


if __name__=='__main__':
    run_agent_collaboration('사용자 비밀번호를 입력받아 DB에 저장하는 간단한 함수 (보안 고려)')