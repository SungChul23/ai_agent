CREATE TABLE IF NOT EXISTS products (
  product_id SERIAL PRIMARY KEY,
  product_name VARCHAR(120) UNIQUE NOT NULL,
  category VARCHAR(60) NOT NULL,
  price NUMERIC(12,2) NOT NULL,
  cost NUMERIC(12,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
  order_id BIGSERIAL PRIMARY KEY,
  order_date TIMESTAMPTZ NOT NULL,
  product_id INTEGER NOT NULL REFERENCES products(product_id),
  quantity INTEGER NOT NULL CHECK(quantity>0),
  amount NUMERIC(12,2) NOT NULL,
  status VARCHAR(30) NOT NULL CHECK(status IN ('paid','refunded','cancelled'))
);
INSERT INTO products(product_name,category,price,cost) VALUES
('AI 업무자동화 Basic','software',49000,12000),
('AI 업무자동화 Pro','software',99000,25000),
('데이터 분석 패키지','service',150000,50000),
('사내 AI Agent 구축','consulting',1200000,500000),
('RAG 구축 컨설팅','consulting',800000,320000)
ON CONFLICT(product_name) DO NOTHING;
INSERT INTO orders(order_date,product_id,quantity,amount,status)
SELECT * FROM (VALUES
('2026-09-01 10:00+09'::timestamptz,1,3,147000::numeric,'paid'),
('2026-09-01 13:00+09'::timestamptz,2,2,198000::numeric,'paid'),
('2026-09-02 11:20+09'::timestamptz,3,1,150000::numeric,'paid'),
('2026-09-02 15:10+09'::timestamptz,2,4,396000::numeric,'paid'),
('2026-09-03 09:30+09'::timestamptz,4,1,1200000::numeric,'paid'),
('2026-09-03 14:30+09'::timestamptz,1,5,245000::numeric,'paid'),
('2026-09-04 10:15+09'::timestamptz,5,1,800000::numeric,'paid'),
('2026-09-04 17:00+09'::timestamptz,2,1,99000::numeric,'refunded'),
('2026-09-05 12:00+09'::timestamptz,3,3,450000::numeric,'paid')
) v(order_date,product_id,quantity,amount,status)
WHERE NOT EXISTS (SELECT 1 FROM orders);