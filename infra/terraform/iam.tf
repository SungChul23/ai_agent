data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2" {
  name               = "${var.project_name}-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

# SSH 키 없이 Session Manager로 접속 가능
resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

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

resource "aws_iam_role_policy" "agent" {
  name   = "${var.project_name}-agent-policy"
  role   = aws_iam_role.ec2.id
  policy = data.aws_iam_policy_document.agent.json
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2.name
}