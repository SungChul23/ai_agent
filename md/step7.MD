# 목표
- PostgreSQL(Docker compose) / pgvector + bedrock embedding
- PostgreSQL(RDB)에 extension을 설치하여 백터를 컬럼의 타입으로 사용 가능하게 확장
    - 테이블내 특정 컬럼이 백터를 저장할 수 있도록 구성
    - RDB 기능, 백터디비 기능 같이 사용

# 구성
```
/
L docker-compose.yml
L app
    L database.py        : PostgreSQL  접속 커넥션 구성
L steps
    L step7_pgvector.py  : 간단한 텍스트(문장)을 테이블 upsert(insert or update) 처리
```

# 디비 구성
```
# 디비 설치
docker compose up -d


# 연결정보 추가 (postgresql://agent:agent@localhost:5432/agentlab)
.env
app.config.py
```

# 초기 sql 구성
```
/
L sql
    L migrations
        L 001_pgvector.sql
```

# 테이블 구성 및 초기 작업
```
python -m scripts.migrate
---
applied: 001_pgvector.sql


# 확인
docker exec -it agent-postgres psql -U agent -d agentlab
---
psql (16.15 (Debian 16.15-1.pgdg12+2))
Type "help" for help.

# 현재 존재하는 모든 스키마(테이블) 확인
agentlab=# \dt
             List of relations
 Schema |       Name        | Type  | Owner 
--------+-------------------+-------+-------
 public | demo_vectors      | table | agent
 public | schema_migrations | table | agent
(2 rows)

# 구조 확인 -> q로 탈출
agentlab=# \d demo_vectors

# sql 수행
agentlab=# select * from demo_vectors;
 id | content | embedding 
----+---------+-----------
(0 rows)
```


# 실행
```
# 1차 실행(쿼리1)
python -m steps.step7_pgvector
----
환불 정책 [-0.06341178715229034, 0.05073736980557442, ..... ]


# 1차 실행(쿼리1, 쿼리2)
python -m steps.step7_pgvector
----
# 질문 : 상품을 반품하고 싶어요 -> CS 관련 질문
('환불 정책', 0.13145827540506594)   <- cs 관련 샘플에서 가장 높은 점수를 얻음
('월 매출 분석', 0.11051657795906067)
('연차 휴가 규정', 0.013668003375411297)
```

# 쿼리를 통해 데이터 확인
```
select id, content from demo_vectors;
 id |    content     
----+----------------
  1 | 환불 정책
  2 | 연차 휴가 규정
  3 | 월 매출 분석
(3 rows)

select 
    id, content, 
    left(embedding::text, 14) || '...' as embedding
from demo_vectors;
-----
 id |    content     |     embedding     
----+----------------+-------------------
  1 | 환불 정책      | [-0.06341179,0...
  2 | 연차 휴가 규정 | [-0.041086007,...
  3 | 월 매출 분석   | [-0.06644361,-...
```