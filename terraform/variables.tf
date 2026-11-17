variable "aws_region" {
  description = "AWS region to deploy the server"
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type (ARM64 Graviton2)"
  type        = string
  default     = "t4g.micro"
}

variable "github_repo_url" {
  description = "GitHub repository URL containing the pipeline scripts"
  type        = string
  default     = "https://github.com/Ganesh-Srinath/event-pipeline.git"
}