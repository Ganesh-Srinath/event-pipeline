output "instance_public_ip" {
  description = "Public IP address of the EC2 server"
  value       = aws_instance.pipeline_server.public_ip
}

output "ssh_command" {
  description = "Command to SSH into your server"
  value       = "ssh -i event-pipeline-key.pem ubuntu@${aws_instance.pipeline_server.public_ip}"
}