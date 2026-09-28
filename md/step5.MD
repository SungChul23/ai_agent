# 목표
- 앞전 단계에서 프럼프트->업무수행(llm호출)를 하나의 에이전트로 가정
- 에이전트를 여러개 만들어서 협업 -> A2A 표현
- 랭체인의 체인단위 구성을 n개 구성하여 서로 상호 다른 작업 진행도록 구성
- 순차적 협업 패턴 진행
    - 랭체인 완결되는 단위 => 에이전트로 표현
    - 구성 (회차 제한)
        - 신입 개발자 에이전트
        - 전문 리뷰어 에이전트
        - 피드백 반영 에이전트
    - 완성된 코드를 개발

# 구조
```
/
L steps
    L step5_a2a_basic.py
```

# 실행 (응답 토큰은 1200으로 제한됨)
```
python -m steps.step5_a2a_basic
---
목표 사용자 비밀번호를 입력받아 DB에 저장하는 간단한 함수 (보안 고려)
==================================================

[신입 개발자] 코드 작성 중...
---
 ```python
import sqlite3
import bcrypt

def create_connection():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY K ... 
 (코드 생략) 
 ---

[전문 개발자] 코드 검토 중...
---
 # 코드 리뷰

전반적으로 비밀번호 해싱 로직 자체(bcrypt 사용, salt 자동 생성, rounds=12, checkpw 사용)는 잘 되어 있습니다. 하지만 프로덕션 코드로 보기엔 몇 가지 중요한 문제가 있습니다.

## 🔴 심각도 높음

### 1. DB 커넥션마다 새 연결 생성 + 커넥션 누수 위험
```python
def create_connection():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS ...")  # 매번 실행됨
    return conn
```
- 매 호출마다 새 커넥션을 열고 `CREATE TABLE IF NOT EXISTS`를 실행하는 건 비효율적입니다.
- 예외 발생 시(`try` 블록 진입 전, 예: `create_connection()` 자체에서 에러) 커넥션이 닫히지 않을 수 있습니다.
- **개선**: `with sqlite3.connect(...) as conn:` 또는 커넥션 풀/컨텍스트 매니저 패턴 사용, 테이블 생성은 앱 초기화 시 한 번만 수행.

```python
def create_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (...)""")
```

### 2. `except sqlite3.IntegrityError`가 지나치게 광범위
- `IntegrityError`는 UNIQUE 제약 위반뿐 아니라 다른 무결성 오류(FK 등)에도 발생합니다. 지금은 문제없지만, 스키마가 커지면 원인 파악이 어려워집니다.
- **개선**: 에러 메시지를 확인하거나, 로깅에 `str(e)`를 남겨 디버깅 가능하게 하세요.
```python
except sqlite3.IntegrityError as e:
    print(f"[⚠️] 이미 존재하는 사용자명: {username} ({e})")
```

### 3. `print`로 결과/에러를 출력 — 로깅 부재
- 실제 서비스 코드에서 `print`는 부적절합니다. `logging` 모듈로 대체해야 하며, 특히 보안 관련 이벤트(로그인 실패 등)는 감사 로그로 남겨야 합니다.
```python
import logging
logger = logging.getLogger(__name__)
...
logger.info("사용자 '%s' 비밀번호 저장 완료", username)
logger.warning("이미 존재하는 사용자명: %s", username)
```
- **주의**: 비밀번호나 해시 자체를 로그에 남기지 마세요 (지금 코드는 안 남기고 있어서 OK).

## 🟡 개선 권장

### 4. `bcrypt`는 72바이트 제한이 있음
- bcrypt는 입력 비밀번호를 72바이트까지만 사용합니다. 매우 긴 비밀번호를 사용하는 경우 뒷부분이 무시되어 보안성이 떨어질 수 있습니다.
- **개선**: 비밀번호 길이 제한 검증 추가 (예: 8~72자) 또는 사전에 S ... 


[신입 개발자] 피드백 반영하여 수정 중...
최종 결과물
리뷰 감사합니다! 지적하신 부분들을 모두 반영해서 개선했습니다. 특히 커넥션 관리랑 로깅 부분은 제가 너무 안일하게 짰던 것 같아요 🙏

```python
import sqlite3
import bcrypt
import logging
from contextlib import contextmanager

# ── 로깅 설정 ──────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

DB_PATH = "users.db"

# bcrypt는 72바이트까지만 사용하므로 입력 검증에 활용
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 72


# ── DB 초기화 (앱 시작 시 한 번만 호출) ──────────────
def init_db():
    """앱 초기화 시 한 번만 호출해서 테이블 생성"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
    logger.info("DB 초기화 완료 (테이블 확인/생성)")


@contextmanager
def get_connection():
    """
    커넥션을 안전하게 열고 닫는 컨텍스트 매니저.
    예외 발생 시에도 반드시 close() 되도록 보장.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# ── 비밀번호 검증 유틸 ──────────────────────────────
def validate_password_length(plain_password: str) -> None:
    """
    bcrypt는 72바이트까지만 실제로 해싱에 사용함.
    너무 짧거나 너무 길면 명시적으로 에러를 발생시켜 사용자에게 알림.
    """
    pw_bytes_len = len(plain_password.encode('utf-8'))
    if pw_bytes_len < MIN_PASSWORD_LENGTH:
        raise ValueError(f"비밀번호는 최소 {MIN_PASSWORD_LENGTH}자 이상이어야 합니다.")
    if pw_bytes_len > MAX_PASSWORD_LENGTH:
        raise ValueError(f"비밀번호는 {MAX_PASSWORD_LENGTH}바이트(약 72자)를 초과할 수 없습니다.")


# ── 비밀번호 저장 ──────────────────────────────────
def save_user_password(username: str, plain_password: str) -> bool:
    """
    사용자 비밀번호를 안전하게 해싱하여 DB에 저장
    - bcrypt로 salt 자동 생성 + 해싱
    -
----