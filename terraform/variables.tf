
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
