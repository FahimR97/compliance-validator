resource "aws_s3_bucket" "pipeline_artifacts" {
  bucket = "cv-pipeline-artifacts-${random_string.suffix.result}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_codebuild_project" "cv_build" {
  name          = "cv-codebuild-project"
  service_role  = aws_iam_role.codebuild.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:7.0"
    type                        = "LINUX_CONTAINER"
    privileged_mode             = true

    environment_variable {
      name  = "DOCKER_USER"
      value = "/codebuild/docker-username"
      type  = "PARAMETER_STORE"
    }

    environment_variable {
      name  = "DOCKER_PASS"
      value = "/codebuild/docker-password"
      type  = "PARAMETER_STORE"
    }

    environment_variable {
      name  = "AWS_DEFAULT_REGION"
      value = "us-west-2"
    }

    environment_variable {
      name  = "EKS_CLUSTER_NAME"
      value = "cv-eks-cluster"
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "buildspec.yml"
  }

  logs_config {
    cloudwatch_logs {
      group_name = "/aws/codebuild/cv-build"
    }
  }
}
