output "jenkins_instance_id" {
  description = "ID of the Jenkins EC2 instance"
  value       = aws_instance.jenkins.id
}

output "k3s_instance_id" {
  description = "ID of the k3s EC2 instance"
  value       = aws_instance.k3s.id
}

output "jenkins_private_ip" {
  description = "Private IP of Jenkins instance"
  value       = aws_instance.jenkins.private_ip
}

output "k3s_private_ip" {
  description = "Private IP of k3s instance"
  value       = aws_instance.k3s.private_ip
}
