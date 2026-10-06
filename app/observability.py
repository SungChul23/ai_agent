'''
랭스미스 상태 체크
'''
import os

def status():
    return {
        "langsmith tracing" : os.getenv("LANGSMITH_TRACING"),
        "project"           : os.getenv("LANGSMITH_PROJECT", ""),
        "API exist"         : bool(os.getenv("LANGSMITH_API_KEY"))
    }