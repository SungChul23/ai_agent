"""sql/migrations의 SQL 파일을 순서대로 한 번씩 적용하는 마이그레이션 도구입니다."""

from pathlib import Path
import psycopg
from app.config import DATABASE_URL

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "sql" / "migrations"

def main():
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations(name TEXT PRIMARY KEY, applied_at TIMESTAMPTZ DEFAULT NOW())")
        # 이미 적용한 파일 이름을 조회해 같은 migration을 다시 실행하지 않는다.
        done = {r[0] for r in conn.execute("SELECT name FROM schema_migrations")}
        # 파일명 숫자 prefix(001, 002...) 순으로 적용한다.
        for path in sorted(MIGRATIONS.glob("*.sql")):
            if path.name in done:
                continue
            conn.execute(path.read_text(encoding="utf-8"))
            conn.execute("INSERT INTO schema_migrations(name) VALUES(%s)", (path.name,))
            print("applied:", path.name)

if __name__ == "__main__":
    main()