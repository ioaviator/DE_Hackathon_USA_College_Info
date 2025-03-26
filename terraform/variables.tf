
variable "resource_group_name" {
  description = "resource group container for all deployed azure services"
  default     = "DE_hackathon"
}

variable "location" {
  default = "Central US"
}

variable "storage_account_name" {
  default = "top1000usaschools"
}

variable "db_admin_login" {
  type      = string
  sensitive = true
  default   = "adminadmin"
}

variable "db_admin_pass" {
  type      = string
  sensitive = true
  default   = "12345678He"
}