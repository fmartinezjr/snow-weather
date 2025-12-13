variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
}

variable "phone_number" {
  description = "Phone number to receive SMS alerts in E.164 format"
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
