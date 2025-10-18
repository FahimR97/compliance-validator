variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  default     = "ami-0360c520857e3138f"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "key_name" {
  description = "EC2 Key Pair name"
  type        = string
  default     = "compliance-validator-keypair"
}

variable "subnet_id" {
  description = "Subnet ID for EC2 instances"
  type        = string
  default     = "subnet-06e28ce9bfc2dea0e"
}

variable "jenkins_security_group_ids" {
  description = "Security group IDs for Jenkins instance"
  type        = list(string)
  default     = ["sg-01486d90612c22aee"]
}

variable "k3s_security_group_ids" {
  description = "Security group IDs for k3s instance"
  type        = list(string)
  default     = ["sg-0ced4261bc7ac1754"]
}
