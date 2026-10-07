# Amazon Linux 2023 ec2 구성, bootstrap.sh로 user_data 전달 처리
# 인프라 생성후 실제 서비스 자동 설치
# DB 초기화(sql 마이그레이션(테이블 생성=> 데이터 삽입))
# 컨테이너 실행

# 리눅스 정보 획득
data "aws_ssm_parameter" "al2023_ami" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# 인스턴스 구성
resource "aws_instance" "agent" {
  # 이미지 -> 최신 아마존 리눅스 2023 AMI ID 사용
  ami = data.aws_ssm_parameter.al2023_ami.value

  # ec2 인스턴스 유형
  instance_type = var.ec2_instance_type

  # 서브넷 ID, EC2 배치 -> 0을 지정해서 사용(설정)
  subnet_id = aws_subnet.public[0].id

  # 보안그룹
  vpc_security_group_ids = [aws_security_group.ec2.id]

  # AWS 다른 서비스 API 호출 (ec2 객체 횏득, bedrock 모델 호출, ssm parameter db url획득)
  iam_instance_profile = aws_iam_instance_profile.ec2.name



}