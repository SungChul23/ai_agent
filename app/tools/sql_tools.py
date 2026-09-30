'''
- 데이터베이스를 대상으로 특정 데이터를 추출, 작업하는 sql 도구 구성
- 패턴화된 작업을 도구화 하여 에이전트가 자율적으로 사용하도록 구성
'''
from langchain_core.tools import tool
from app.database import connect

@tool
def sales_summary(start_date: str, end_date: str) -> str:
    '''
        특정 날짜 범위(YYY-MM-DD) 내에서 결제 완료 매출과 주문 건수를 조회한다 => 집계
    '''
    with connect() as conn, conn.cursor() as cur:
        # 결제 완료된 건만 대상으로 시작일, 종료일까지 대상
        sql = """
            select
                COALESCE(sum(amount), 0),
                count(*)
            from orders
            where 
                status='paid'
                and order_date >= %s::date
                and order_date < (%s::date + INTERVAL '1 day')
            ;
        """
        params = (start_date, end_date)
        cur.execute(sql, params)
        revenue, count = cur.fetchone()
    return f"revenue={revenue}, orders={count}, range={start_date}~{end_date}"

@tool
def top_products(start_date: str, end_date: str, limit:int=3) -> str:
    '''
        특정 날짜 범위(YYY-MM-DD) 내에서 결제 완료된 매출 기준 상위 제품 조회
        제품명(name), 수량(qty), 매출액(revenue)를 추출한다
        - 조인, 조건, 집계, 정렬, 제한
    '''
    with connect() as conn, conn.cursor() as cur:
        sql = """
            select
                p.product_name,
                sum(o.quantity),
                sum(o.amount)
            from orders o
            join products p
                using (product_id)
            where 
                status='paid'
                and order_date >= %s::date
                and order_date < (%s::date + INTERVAL '1 day')
            group by
                p.product_id,
                p.product_name
            order by
                sum(o.amount) desc
            limit %s
            ;
        """
        params = (start_date, end_date, max(1, min(limit, 9) ))
        cur.execute(sql, params)
        rows = cur.fetchall()
    return "\n".join( f"{i+1}. {name}: qty={qty}, revenue={revenue}" for i, (name, qty, revenue) in enumerate(rows) )