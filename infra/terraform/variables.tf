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