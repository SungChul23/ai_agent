-- ==================================
-- 1. 원본 문서 정보를 저장하는 테이블
--    문저 자체, 메타 정보
--    documents
-- ==================================
CREATE TABLE IF NOT EXISTS documents (

    -- 문서 내부 PK
    -- BIGSERIAL: 값이 자동으로 1씩 증가
    id BIGSERIAL PRIMARY KEY,

    -- 문서를 식별하기 위한 업무용 코드
    -- UNIQUE: 동일한 문서 코드 중복 등록 방지
    document_code VARCHAR(100) UNIQUE NOT NULL,

    -- 문서 담당 부서
    -- 예: 인사팀, 재무팀, 개발팀
    department VARCHAR(50) NOT NULL,

    -- 문서 분류
    -- 예: 규정, 매뉴얼, 가이드, 정책
    category VARCHAR(100) NOT NULL,

    -- 문서 제목
    title TEXT NOT NULL,

    -- 문서 출처
    -- 예: 사내문서, Notion, PDF, URL 등
    source TEXT NOT NULL,

    -- 문서 버전
    -- 예: v1.0, 2026-01
    version VARCHAR(30),

    -- 문서 효력 발생일
    effective_date DATE,

    -- DB에 문서가 등록된 시간
    -- 값이 없으면 현재 시간을 자동 저장
    created_at TIMESTAMPTZ DEFAULT NOW()
);



-- ==================================
-- 2. 문서를 작은 단위(chunk)로 나눠서 저장하는 테이블
--    RAG 수행시 chunk 단위로 검색, 하나의 문서는 n개의 chunk 분할
--    document_chunks
-- ==================================
CREATE TABLE IF NOT EXISTS document_chunks (

    -- chunk 내부 PK
    id BIGSERIAL PRIMARY KEY,

    -- 이 chunk가 어떤 문서에 속하는지 연결
    -- documents.id를 참조하는 Foreign Key
    document_id BIGINT NOT NULL
        REFERENCES documents(id)
        ON DELETE CASCADE,
        -- 원본 documents가 삭제되면
        -- 해당 문서의 chunk도 자동 삭제

    -- 문서 내 chunk 순서
    -- 예: 0, 1, 2, 3 ...
    chunk_index INTEGER NOT NULL,

    -- 실제 chunk 텍스트
    -- RAG 검색 후 LLM에게 전달할 실제 내용
    content TEXT NOT NULL,

    -- chunk 내용을 임베딩한 벡터
    -- 1024차원 임베딩 모델을 사용하는 구조
    -- pgvector extension 필요
    embedding VECTOR(1024) NOT NULL,

    -- chunk별 추가 정보
    -- JSON 형태이므로 필요한 속성을 유연하게 추가 가능
    -- 예:
    -- {"page": 3, "section": "휴가 규정"}
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- chunk 생성 시간
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- 하나의 문서에서 동일한 chunk_index 중복 방지
    UNIQUE(document_id, chunk_index)
);


-- ==================================
-- 3. 문서 필터 검색용 인덱스
--    부서, 카테고리, 적용일 기준 문서 필터 검색용 복합 인덱스
-- ==================================
create index if not exists idx_documents_filters
on documents(department, category, effective_date)

-- ==================================
-- 4. chunk 메타 정보 검색용 인덱스
--    jonb 타입의 컬럼이므로, jsonb 내부값,키등을 빠른 검색을 하기 위해  gin 인덱스 사용
-- ==================================
create index if not exists idx_chunks_metadata
on document_chunks using gin(metadata)

-- ==================================
-- 5. 임베딩 백터 유사도 검색용 인덱스
--    코사인 거리 유사도 기반 백터 검색시 사용있도록 hnsw 인덱스 반영
-- ==================================
create index if not exists idx_chunks_hnsw
on document_chunks using hnsw(embedding vector_cosine_ops)