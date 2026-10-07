#!/bin/bash
# ============================================================
# EC2 Bootstrap Script
# Terraform의 user_data로 EC2 최초 부팅 시 자동 실행됩니다.
# 목표: Docker 설치 → 소스 다운로드 → 환경변수 구성 → 이미지 빌드
#      → DB Migration → RAG 적재 → API 실행 → Health Check
# ============================================================
# -E: ERR trap 상속 / -e: 오류 즉시 종료 / -u: 미정의 변수 오류 / pipefail: 파이프 오류 감지
set -Eeuo pipefail
# 모든 실행 로그를 파일과 EC2 console에 동시에 남깁니다.
exec > >(tee /var/log/agent-bootstrap.log | logger -t user-data -s 2>/dev/console) 2>&1

APP_DIR=/opt/agent-course
IMAGE_NAME=agent-course:latest
CONTAINER_NAME=agent-course

# RDS 준비, S3/SSM 호출, API 시작처럼 시간이 필요한 작업을 재시도하는 공통 함수
retry() {
  local attempts="$1"; shift
  local sleep_seconds="$1"; shift
  local n=1
  until "$@"; do
    if [ "$n" -ge "$attempts" ]; then
      echo "ERROR: command failed after $n attempts: $*" >&2
      return 1
    fi
    echo "retry $n/$attempts: $*" >&2
    n=$((n+1))
    sleep "$sleep_seconds"
  done
}

echo "[1/8] Docker / AWS CLI 설치"
# Amazon Linux 2023에는 curl-minimal이 기본 설치되어 있습니다.
# 일반 curl 패키지를 함께 설치하면 충돌할 수 있으므로 별도 설치하지 않습니다.
dnf install -y docker awscli unzip
systemctl enable --now docker

# SSM Agent는 AL2023 AMI에 기본 포함되지만 명시적으로 활성화
systemctl enable --now amazon-ssm-agent || true

echo "[2/8] 프로젝트 소스 다운로드"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"
cd "$APP_DIR"
retry 12 10 aws s3 cp "s3://${source_bucket}/${source_key}" /tmp/agent-course.zip --region "${aws_region}"
unzip -q /tmp/agent-course.zip -d "$APP_DIR"

echo "[3/8] RDS 접속정보 조회 및 .env 생성"
DATABASE_URL=$(retry 12 10 aws ssm get-parameter \
  --name "${database_url_parameter}" \
  --with-decryption \
  --query 'Parameter.Value' \
  --output text \
  --region "${aws_region}")

cat > .env <<ENVEOF
AWS_REGION=${aws_region}
BEDROCK_CHAT_MODEL=${chat_model}
BEDROCK_EMBED_MODEL=${embed_model}
DATABASE_URL=$DATABASE_URL
USER_ID=${user_id}
LANGSMITH_TRACING=false
LANGSMITH_PROJECT=agent-course-lab
ENVEOF
chmod 600 .env

echo "[4/8] Agent Docker image build"
docker build -t "$IMAGE_NAME" .

echo "[5/8] RDS 준비 대기 + SQL migration 실행"
# migrate.py가 연결 성공할 때까지 재시도합니다.
# 실행 순서: 001 pgvector -> 002 documents -> 003 business(seed 포함)
#          -> 004 refunds(seed 포함) -> 005 memory
retry 30 10 docker run --rm --env-file .env "$IMAGE_NAME" python -m scripts.migrate

echo "[6/8] RAG 문서 embedding + 초기 데이터 적재"
retry 5 15 docker run --rm --env-file .env "$IMAGE_NAME" python -m app.ingestion.ingest

echo "[7/8] FastAPI/LangGraph Agent container 실행"
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  --env-file .env \
  -p 8000:8000 \
  "$IMAGE_NAME"

echo "[8/8] Health check"
retry 30 5 curl -fsS http://127.0.0.1:8000/health
echo
echo "DEPLOYMENT COMPLETE"