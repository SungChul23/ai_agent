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

# 결과
```
    목표 사용자 비밀번호를 입력받아 DB에 저장하는 간단한 함수 (보안 고려)
    ==================================================

    [신입 개발자] 코드 작성 중...
    ---
    ## 비밀번호 저장 함수 (bcrypt 사용)

    ```python
    import bcrypt
    import sqlite3

    def hash_password(plain_password: str) -> bytes:
        """비밀번호를 salt와 함께 해싱"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(p ... 
    (코드 생략) 
    ---

    [전문 개발자] 코드 검토 중...
    ---
    # 코드 리뷰

    전반적으로 bcrypt 사용법과 SQL Injection 방지(파라미터 바인딩)는 잘 지켜졌습니다. 다만 실무 적용 전 짚어야 할 문제들이 있습니다.

    ## 🔴 심각도 높음

    ### 1. DB 연결 관리 — 예외 발생 시 리소스 누수 위험
    `save_user_password`에서 `CREATE TABLE` 실행 중 예외가 나면 `conn.close()`가 호출되지 않습니다. `try/finally`나 `with` 구문으로 감싸야 합니다.

    ```python
    def save_user_password(username: str, plain_password: str, db_path: str = "users.db"):
        hashed_pw = hash_password(plain_password)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash BLOB NOT NULL
                )
            """)
            try:
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed_pw)
                )
                conn.commit()
                print(f"[성공] '{username}' 저장 완료")
            except sqlite3.IntegrityError:
                print(f"[실패] '{username}' 이미 존재하는 사용자")
    ```
    (단, sqlite3의 `with`는 커밋/롤백만 자동 처리하고 연결을 닫지는 않으니, 완전한 자동 종료를 원하면 `contextlib.closing`을 함께 써야 합니다.)

    ### 2. 비밀번호 정책 검증 부재
    길이/복잡도 검사가 전혀 없습니다. bcrypt는 입력을 72바이트까지만 처리하므로, 그 이상 입력해도 잘려서 해싱됩니다 — 사용자가 인지하지 못한 채 보안이 약화될 수 있습니다.

    ```python
    def hash_password(plain_password: str) -> bytes:
        if not (8 <= len(plain_password) <= 72):
            raise ValueError("비밀번호는 8~72자여야 합니다.")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    ```

    ### 3. 예외 처리가 `IntegrityError`만 커버
    DB 파일 권한 문제, disk full, 락 경합(`sqlite3.OperationalError`) 등은 처리되지 않고 그대로 예외가 위로 전파됩니다. 최소한 로깅 후 재던지기를 권장합니다.

    ## 🟡 개선 권장

    ### 4. 매 호출마다 `CREATE TABLE IF NOT EXISTS` 실행 — 비효율
    로그인/저장할 때마다 테이블 존재 확인 쿼리를 실행하는 건 불필요한 오버헤드입니다. 앱 초기화 시 한 번만 실행하는 `init_db()` 함수로 분리하세요.

    ```python
    def init_db(db_path: str = "users.db"):
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTE ... 


    [신입 개발자] 피드백 반영하여 수정 중...
    최종 결과물
    ```python
    import bcrypt
    import sqlite3
    import logging
    from contextlib import closing

    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    def init_db(db_path: str = "users.db"):
        """앱 초기화 시 한 번만 호출하여 테이블을 생성"""
        with closing(sqlite3.connect(db_path)) as conn:
            with conn:  # commit/rollback 자동 처리
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash BLOB NOT NULL
                    )
                """)
        logger.info("DB 초기화 완료: %s", db_path)


    def hash_password(plain_password: str) -> bytes:
        """비밀번호를 salt와 함께 해싱 (정책 검증 포함)"""
        if not isinstance(plain_password, str):
            raise TypeError("비밀번호는 문자열이어야 합니다.")

        # bcrypt는 72바이트까지만 처리하므로, 그 이상은 명시적으로 거부
        encoded = plain_password.encode('utf-8')
        if not (8 <= len(plain_password) <= 72) or len(encoded) > 72:
            raise ValueError("비밀번호는 8~72자(바이트 기준 72바이트 이하)여야 합니다.")

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(encoded, salt)
        return hashed


    def save_user_password(username: str, plain_password: str, db_path: str = "users.db") -> bool:
        """사용자 비밀번호를 해싱하여 DB에 저장

        반환값: 저장 성공 여부(bool)
        """
        if not username or not username.strip():
            raise ValueError("username은 비어있을 수 없습니다.")

        try:
            hashed_pw = hash_password(plain_password)
        except (ValueError, TypeError) as e:
            logger.warning("비밀번호 정책 위반: %s", e)
            raise

        try:
            with closing(sqlite3.connect(db_path)) as conn:
                with conn:  # 성공 시 commit, 예외 시 rollback 자동 처리
                    try:
                        conn.execute(
                            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                            (username, hashed_pw)
                        )
                    except sqlite3.IntegrityError:
                        logger.info("'%s' 이미 존재하는 사용자", username)
                        return False
            logger.info("'%s' 저장 완료", username)
            return True

        except sqlite3.OperationalError as e:
            # DB 파일 권한 문제, disk full, 락 경합 등
            logger.error("DB 작업 중 오류 발생 (username=%s): %s", username, e)
            raise
        except sqlite3.Error as e:
            logger.error("예상치 못한 sqlite3 오류 (username=%s): %

```