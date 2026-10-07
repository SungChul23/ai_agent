# 가용영역 조회
data "aws_availability_zones" "available" {
  # 현재(리전 기준) 사용 가능한 availability zone만 조회
  state = "available"
}
# VPC 생성
resource "aws_vpc" "main" {
  # IPV4 CIDR 가용범위
  cidr_block = var.vpc_cidr
  # DNS 기능 허용
  enable_dns_support   = true # dns 해석 기능 활성화
  enable_dns_hostnames = true # VPC 내에서 dns_hostnames 사용 허가
  # 태그
  tags = {
    Name = "${var.project_name}-vpc"
  }
}
# IGW 생성
resource "aws_internet_gateway" "main" {
  # 어느 vpc에 적용(혹은 속하는가)
  vpc_id = aws_vpc.main.id
  # 식별 태그
  tags = {
    Name = "${var.project_name}-igw"
  }
}
# 서브넷 생성
resource "aws_subnet" "public" {
  # 동일한 형태의 리소스를 몇개 구성할 것인가?
  count = 2
  # 어떤 vpc에 속하는가?
  vpc_id = aws_vpc.main.id
  # 라우팅시 사용할 IPV4의 cidr 범위
  # 10.30.1.0/24, 10.30.2.0/24 <- 서브넷의 각각 cidr 범위
  cidr_block = cidrsubnet(var.vpc_cidr, 8, count.index + 1)
  # 가용영역 -> 서브넷별로 다른 가용영역 배치
  availability_zone = data.aws_availability_zones.available.names[count.index]
  # public IP 자동할당 -> 인프라 구축되면 해당 http://IP:8000로 접속
  map_public_ip_on_launch = true
  # 식별 태그
  tags = {
    Name = "${var.project_name}-public-${count.index + 1}"
  }
}
# 라우트테이블 생성
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    # 라우팅할 CIDR 블럭 범위
    cidr_block = "0.0.0.0/0"
    # 인터넷 트레픽 방향 -> IGW 전달
    gateway_id = aws_internet_gateway.main.id
  }
  tags = {
    Name = "${var.project_name}-public-rt"
  }
}
# 서브넷, IGW 연결, 라우트 할당
resource "aws_route_table_association" "public" {
  # 리소스 2개(서브넷) 지정
  count = 2
  # 서브넷 ID
  subnet_id = aws_subnet.public[count.index].id
  # 라우트테이블 연결
  route_table_id = aws_route_table.public.id
}