-- agent 메모리, 사용자를 기억하도록
-- 실 서비스라면 사용자의 id를 같이 저장
CREATE TABLE IF NOT EXISTS agent_memories (    
    id BIGSERIAL PRIMARY KEY,
    -- 사용자별
    used_id VARCHAR(100) NOT NULL,
    -- 메모리 타입
    memory_type VARCHAR(30) NOT NULL,    
    -- 저장할 내용
    content TEXT NOT NULL,    
    -- 저장한 내용에 대한 백터화값
    embedding VARCHAR(1024) NOT NULL,
    -- 중요도
    importance DOUBLE PRECISION NOT NULL DEFAULT 0.5,    
    -- 최초 저장일
    created_at TIMESTAMPTZ DEFAULT NOW(),
    -- 엑세스 시간정보
    last_accessed_at TIMESTAMPTZ
);
-- user_id 조건으로 특정 사용자의 기억을 빠르게 조회
create index if not exists idx_memories_user
on agent_memories(used_id);

-- 백터의 코사인 유사도로 빠른 검색 지원
-- 의미 있는 유사한 기억 검색 속도 향상
create index if not exists idx_memories_hnsw
on agent_memories using hnsw(embedding vector_cosine_ops);