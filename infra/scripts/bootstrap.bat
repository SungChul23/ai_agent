@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================================================
REM Branch 20 - Windows Bootstrap
REM Prerequisites:
REM   - AWS CLI installed and authenticated
REM   - Docker installed and running
REM   - unzip is handled by PowerShell Expand-Archive
REM
REM Required environment variables:
REM   SOURCE_BUCKET
REM   SOURCE_KEY
REM   AWS_REGION
REM   DATABASE_URL_PARAMETER
REM   CHAT_MODEL
REM   EMBED_MODEL
REM ============================================================

REM 1. Required variable check
for %%V in (
    SOURCE_BUCKET
    SOURCE_KEY
    AWS_REGION
    DATABASE_URL_PARAMETER
    CHAT_MODEL
    EMBED_MODEL
) do (
    if "!%%V!"=="" (
        echo [ERROR] Environment variable %%V is not set.
        exit /b 1
    )
)

REM 2. Deployment directory
set "APP_DIR=C:\agent-course"
set "ZIP_FILE=%TEMP%\agent-course.zip"

if not exist "%APP_DIR%" mkdir "%APP_DIR%"

REM 3. Download project ZIP from S3
aws s3 cp "s3://%SOURCE_BUCKET%/%SOURCE_KEY%" "%ZIP_FILE%" --region "%AWS_REGION%"
if errorlevel 1 exit /b 1

REM Existing files are overwritten
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%APP_DIR%' -Force"
if errorlevel 1 exit /b 1

cd /d "%APP_DIR%"

REM 4. Read DATABASE_URL from SSM Parameter Store
for /f "usebackq delims=" %%A in (`aws ssm get-parameter --name "%DATABASE_URL_PARAMETER%" --with-decryption --query "Parameter.Value" --output text --region "%AWS_REGION%"`) do (
    set "DATABASE_URL=%%A"
)

if "%DATABASE_URL%"=="" (
    echo [ERROR] Failed to read DATABASE_URL from SSM.
    exit /b 1
)

REM 5. Create Agent environment file
(
    echo AWS_REGION=%AWS_REGION%
    echo BEDROCK_CHAT_MODEL=%CHAT_MODEL%
    echo BEDROCK_EMBED_MODEL=%EMBED_MODEL%
    echo DATABASE_URL=%DATABASE_URL%
    echo AGENT_USER_ID=student-01
    echo LANGSMITH_TRACING=false
    echo LANGSMITH_PROJECT=agent-course-lab
) > .env

REM 6. Build Agent Docker image
docker build -t agent-course:latest .
if errorlevel 1 exit /b 1

REM 7. Configure RDS Schema / pgvector
docker run --rm --env-file .env agent-course:latest python -m scripts.migrate
if errorlevel 1 exit /b 1

REM 8. Ingest RAG documents
docker run --rm --env-file .env agent-course:latest python -m lessons.step07_document_ingestion
if errorlevel 1 exit /b 1

REM 9. Run FastAPI + LangGraph Agent
docker rm -f agent-course >nul 2>&1

docker run -d ^
  --name agent-course ^
  --restart unless-stopped ^
  --env-file .env ^
  -p 8000:8000 ^
  agent-course:latest

if errorlevel 1 exit /b 1

echo.
echo ============================================
echo Agent service deployment completed.
echo http://localhost:8000/health
echo http://localhost:8000/docs
echo ============================================

endlocal