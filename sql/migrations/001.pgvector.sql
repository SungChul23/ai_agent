-- 1. pgvector 확장을 활성화 처리
--    vector 단위 저장/검색 기능 사용가능해짐
--    차후, SQL을 이용하여 RAG 처리시 사용. 하나의 타입으로 관리
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. 테이블 생성
CREATE TABLE IF NOT EXISTS demo_vectors (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL UNIQUE,
    embedding VECTOR(1024) NOT NULL
);