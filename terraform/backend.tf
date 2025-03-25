
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "backend_tf"
    storage_account_name = "hackathonstatebackend"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
