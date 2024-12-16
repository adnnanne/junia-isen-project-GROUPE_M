variable "resource_group_name" {
  default = "rg" # Name of the Resource Group
}

variable "location" {
  default = "France Central" # Set to France Central
}

variable "prefix" {
  default = "flask-api" # Prefix for resource names
}

variable "log_analytics_workspace_name" {
  description = "The name of the Log Analytics Workspace."
  type        = string
  default     = "log-analytics"
}

variable "retention_in_days" {
  description = "The retention period for logs in days."
  type        = number
  default     = 30
}

variable "monitoring_categories" {
  description = "A list of monitoring log categories to enable."
  type        = list(string)
  default     = ["AppServiceHTTPLogs", "AllMetrics"]
}

