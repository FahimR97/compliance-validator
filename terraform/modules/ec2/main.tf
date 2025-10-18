resource "aws_instance" "jenkins" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name              = var.key_name
  subnet_id             = var.subnet_id
  vpc_security_group_ids = var.jenkins_security_group_ids

  tags = {
    Name = "cv-jenkins-001"
  }
}

resource "aws_instance" "k3s" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name              = var.key_name
  subnet_id             = var.subnet_id
  vpc_security_group_ids = var.k3s_security_group_ids

  tags = {
    Name = "cv-k3s-001"
  }
}
