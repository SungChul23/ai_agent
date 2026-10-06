# Terraform 및 Provider 버전 고정
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    # 프로젝트 소스를 ZIP으로 만들기 위해 사용
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.7"
    }
    # 배포용 S3 Bucket 이름 충돌 방지용 suffix 생성
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
}