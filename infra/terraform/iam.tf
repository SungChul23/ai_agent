# EC2에서 엑세스키 없이 S3, SSM Parameter Store, Bedrock 사용
# Session Manager 접속 가능
# EC2 기본 정책 사용

# ec2 권한 획득
data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}
# role 생성
resource "aws_iam_role" "ec2" {
  # 고유한 이름
  name               = "${var.project_name}-ec2-role"
  # 정책 ec2.amazonaws.com 반영
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

# SSH 키 없이 Session Manager로 접속 가능
resource "aws_iam_role_policy_attachment" "ssm_core" {
  # role 지정
  role       = aws_iam_role.ec2.name
  # AmazonSSMManagedInstanceCore 정책 반영 -> SSM 신뢰 정책 연결
  # EC2에서 IAM Role 사용 -> SSM 사용
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# EC2에서 새로운 작업 할수 있도록 
# s3에서 업로드된 객체 획득 (소스코드 획득=>설치)
# ssm parameter에서 db 접속 url을 획득 -> RDS 접속 가능
# bedrock의 모델 호출 => Agent 기능 사용
data "aws_iam_policy_document" "agent" {
  statement {
    sid = "ReadDeploymentSource"
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.deploy.arn}/*"]
  }

  statement {
    sid = "ReadDatabaseUrl"
    actions = ["ssm:GetParameter"]
    resources = [aws_ssm_parameter.database_url.arn]
  }

  statement {
    sid = "UseBedrock"
    actions = [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream"
    ]
    resources = ["*"]
  }
}
# role에 정책 반영, 정책을 구성 (위에서 준비한 ec3, ssm, bedrock)
resource "aws_iam_role_policy" "agent" {
  name   = "${var.project_name}-agent-policy"
  role   = aws_iam_role.ec2.id
  policy = data.aws_iam_policy_document.agent.json
}
# 최정 반영하여 프로필 구성
resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2.name
}