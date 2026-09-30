# 목표
- 랭체인 Tool 구성
- SQL 수행 TOOL, RAG TOOL,... 향후 외부도구 연결(MCP)(노션,슬렉, 카톡, 외부s/w, 데탑s.w, 뱅킹)
- 도구 구성 하여 에이전트가 자율적으로 판단하여 도구를 사용하도록 구성 => 랭그래프 출현

# 구조
```
/
L app
    L tools
        L __init__.py
        L rag_tools.py      : rag를 도구로 사용할수 있는 내용 적제 -> @tool
        L sql_tools.py      : sql를 도구로 사용할수 있는 내용 적제 -> @tool
L steps
    L step11_tools.py       : 툴 사용 테스트 코드
L sql
    L 003_business.sql      : sql 툴을 위한 대상 태이블과 더미 데이터

```

# 테이블 생성및 데이터 삽입
```
python -m scripts.migrate
----
agentlab=# \dt
             List of relations
 Schema |       Name        | Type  | Owner 
--------+-------------------+-------+-------
 public | demo_vectors      | table | agent
 public | document_chunks   | table | agent
 public | documents         | table | agent
 public | orders            | table | agent
 public | products          | table | agent
 public | schema_migrations | table | agent
(6 rows)

agentlab=# select * from products;
 product_id |    product_name     |  category  |   price    |   cost    
------------+---------------------+------------+------------+-----------
          1 | AI 업무자동화 Basic | software   |   49000.00 |  12000.00
          2 | AI 업무자동화 Pro   | software   |   99000.00 |  25000.00
          3 | 데이터 분석 패키지  | service    |  150000.00 |  50000.00
          4 | 사내 AI Agent 구축  | consulting | 1200000.00 | 500000.00
          5 | RAG 구축 컨설팅     | consulting |  800000.00 | 320000.00
(5 rows)

agentlab=# select * from orders;
 order_id |       order_date       | product_id | quantity |   amount   |  status  
----------+------------------------+------------+----------+------------+----------
        1 | 2026-09-01 01:00:00+00 |          1 |        3 |  147000.00 | paid
        2 | 2026-09-01 04:00:00+00 |          2 |        2 |  198000.00 | paid
        3 | 2026-09-02 02:20:00+00 |          3 |        1 |  150000.00 | paid
        4 | 2026-09-02 06:10:00+00 |          2 |        4 |  396000.00 | paid
        5 | 2026-09-03 00:30:00+00 |          4 |        1 | 1200000.00 | paid
        6 | 2026-09-03 05:30:00+00 |          1 |        5 |  245000.00 | paid
        7 | 2026-09-04 01:15:00+00 |          5 |        1 |  800000.00 | paid
        8 | 2026-09-04 08:00:00+00 |          2 |        1 |   99000.00 | refunded
        9 | 2026-09-05 03:00:00+00 |          3 |        3 |  450000.00 | paid
(9 rows)
```