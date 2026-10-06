FROM python:3.12-slim
WORKDIR /app

# 패키지 목록 갱신
# PostgreSQL 클라이언트 라이브러리 설치 -> 불필요한 목록 제거 -> 용량 다이어트
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python", "app.service:app", "--host", "0.0.0.0", "--port", "8000"]