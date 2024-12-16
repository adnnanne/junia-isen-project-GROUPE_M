variable "resource_group_name" {
  default = "rg" # Name of the Resource Group
}

variable "location" {
  default = "France Central" # Set to France Central
}

variable "prefix" {
  default = "flask-api" # Prefix for resource names
}

variable "key_vault_name" {
  description = "The name of the Azure Key Vault."
  type        = string
  default     = "my-key-vault"
}

variable "tenant_id" {
  description = "The Azure Active Directory tenant ID."
  type        = string
}

variable "secret_names" {
  description = "A map of secret names and values to store in the Key Vault."
  type        = map(string)
  default     = {}
}
