resource "azurerm_resource_group" "hackathonresource" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "hackathonstorage" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}


resource "azurerm_storage_container" "rawstoragecontainer" {
  name                  = "raw"
  storage_account_name  = var.storage_account_name
  container_access_type = "private"
}

