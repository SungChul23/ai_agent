# EC2 -> 외부에서 8000 포트로 접근, SSH x, SSM 접근
# RDS -> EC2 Security Group 여기만 접근 가능, 5432만 허용

# EC2 시큐리티 그룹
resource "aws_security_group" "ec2" {
  name = "${var.project_name}-ec2-sg"
  description = "Agent API Security Group"
  vpc_id = aws_vpc.main.id
  # 외부에서 SG를 통하여 접근하는 트레픽 규칙
  ingress = {
    description = "FastAPI"
    # 허용할 포트 범위, 시작 포트
    from_port = 8000
    # 허용할 포트 범위, 마지막 포트
    to_port   = 8000
    # 허용 프로토콜
    protocol  = "tcp"
    # 접근 허용 가능한 IPv4 cidr -> 0.0.0.0/0
    cidr_blocks = [var.api_cidr]
  }
  # 아웃바운드
  egress = {
    # 모든 포트 허용
    from_port = 0
    to_port   = 0
    # 모든 프로토콜
    protocol  = "-1"    
    # 모든 IP로 아웃바운드 허가
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { 
    Name = "${var.project_name}-ec2-sg"
  }
}

# RDS 시큐리티 그룹
resource "aws_security_group" "rds" {
  name = "${var.project_name}-rds-sg"
  description = "PostgreSQL Only From Agent EC2 Security Group"
  vpc_id = aws_vpc.main.id
  ingress = {
    description = "PostgreSQL from EC2"
    # 허용할 포트 범위, 시작 포트
    from_port = 5432
    # 허용할 포트 범위, 마지막 포트
    to_port   = 5432
    # 허용 프로토콜
    protocol  = "tcp"
    # 접근 허용 가능한 특정 시크리티 그룹
    # 권한이 있는 리소스(ec2가 aws_security_group.ec2 그룹에 속함) 에서 접근 가능
    security_groups = [aws_security_group.ec2.id]
  }
  # 아웃바운드
  egress = {
    # 모든 포트 허용
    from_port = 0
    to_port   = 0
    # 모든 프로토콜
    protocol  = "-1"    
    # 모든 IP로 아웃바운드 허가
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { 
    Name = "${var.project_name}-rds-sg"
  }
}