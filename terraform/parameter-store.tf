resource "aws_ssm_parameter" "docker_username" {
  name  = "/codebuild/docker-username"
  type  = "SecureString"
  value = "fahimr97"
}

resource "aws_ssm_parameter" "docker_password" {
  name  = "/codebuild/docker-password"
  type  = "SecureString"
  value = "PLACEHOLDER_CHANGE_ME"
}
