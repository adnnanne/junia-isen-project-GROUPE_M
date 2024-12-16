variable "resource_group_name" {
  default = "app_resource_group" # Name of the Resource Group
}

variable "location" {
  default = "France Central" # Set to France Central
}

variable "prefix" {
  default = "flask" # Prefix for resource names
}

variable "sql_server_name" {
  description = "The name of the SQL server"
  type        = string
  default="flaskserver"
}

variable "sql_database_name" {
  description = "The name of the SQL database"
  type        = string
  default="flaskdb"
}

variable "admin_username" {
  description = "The admin username for the SQL server"
  type        = string
  default="admin"
}

variable "admin_password" {
  description = "The admin password for the SQL server"
  type        = string
  default="admin123"
}

variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
  default="admin"
}
variable "storage_container_name" {
  description = "The name of the storage container"
  type        = string
  default="admin"
}

variable "storage_blob_name" {
  description = "The name of the storage blob"
  type        = string
  default="admin"
}

variable "storage_blob_source" {
  description = "The source file for the storage blob"
  type        = string
  default="admin"
}

variable "log_analytics_workspace_name" {
  description = "The name of the Log Analytics Workspace."
  type        = string
  default     = "log-analytics"
}