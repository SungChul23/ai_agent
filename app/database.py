'''
PostgreSQL 연결 담당
psycopg를 이용하여 PostgreSQL에 연결후 pgvector 타입을 등록
python => vector 컬럼을 처리할 수 있도록 구성
'''

import psycopg
from pgvector.psycopg import register_vector
from .config import DATABASE_URL

def connect():
    conn = psycopg.connect(DATABASE_URL)
    register_vector( conn )
    return conn