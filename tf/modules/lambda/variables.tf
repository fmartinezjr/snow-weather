variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
}

variable "email" {
  description = "Email address to receive snow alerts"
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
