# 외부에서 사용 가능한 주소 및 최종 리소스 정보들 출력
output "api_url" {
  description = "FastAPI base URL"
  value       = "http://${aws_instance.agent.public_ip}:8000"
}

output "health_url" {
  description = "서비스 Health Check URL"
  value       = "http://${aws_instance.agent.public_ip}:8000/health"
}

output "chat_url" {
  description = "Agent Chat API URL"
  value       = "http://${aws_instance.agent.public_ip}:8000/chat"
}

output "ec2_public_ip" {
  value = aws_instance.agent.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.address
}

output "ssm_connect_command" {
  description = "SSH key 없이 EC2 접속"
  value       = "aws ssm start-session --target ${aws_instance.agent.id} --region ${var.aws_region}"
}