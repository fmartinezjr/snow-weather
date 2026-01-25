variable "aws_region" {
  description = "AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "snow-weather"
}

variable "email" {
  description = "Email address to receive snow alerts"
  type        = string
}

variable "schedule_expression" {
  description = "EventBridge schedule expression for weather checks"
  type        = string
  default     = "cron(0 */6 * * ? *)" # Every 6 hours
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "snow-weather"
  }
}
