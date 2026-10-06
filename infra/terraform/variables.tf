variable "aws_region" {
  description = "AWS 리전"
  type = string
  default = "us-east-1"
}

# AWS 리소스간 공통 prefix
variable "project_name" {
  description = "프로젝트별 구분값"
  type = string
  default = "agent-de-ai-22"
}

# EC2 관련
# Agent/fastapi
variable "instance_type" {
  description = "에이전트 구동용 ec2"
  type = string
  default = "t3.micro"
}
# FastAPI(8000) 접속 IP cidr
# 편의상 전체 개방
variable "api_cidr" {
  description = "FastAPI용 CIDR"
  type = string
  default = "0.0.0.0/0"
}

# Bedrock Model ID
variable "chat_model" {
  description = "엔트로픽 기본 모델"
  type = string
  default = "us.anthropic.claude-sonnet-5"
}
# 임베딩 모델
variable "embed_model" {
  description = "임베딩 모델"
  type = string
  default = "amazon.titan-embed-text-v2:0"
}
# RDS내에 디비명
variable "db_name" {
  description = "백터 디비명"
  type = string
  default = "agentlab"
}
# RDS내에 사용자명
variable "db_username" {
  description = "백터 디비명 접근 사용자명"
  type = string
  default = "agent"
}
# RDS내에 비밀번호
variable "db_password" {
  description = "RDS 마스터 패스워드"
  type = string
  sensitive = true
}
# RDS 인스턴스 사양
variable "db_instalce_class" {
  description = "RDS 인스턴스 유형"
  type = string
  default = "db.t4g.micro"
}

# VPC 대역
variable "vpc_cidr" {
  description = "VPC CIDR"
  type = string
  default = "10.30.0.0/16"
}

# SSH 관련 (키페어등)
# SSH 접근 IP 대역 => 자기자신 IP