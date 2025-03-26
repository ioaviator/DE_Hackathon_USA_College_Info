resource "azurerm_resource_group" "hackathonresource" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = "hackathon"
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}


resource "azurerm_storage_container" "storagecontainer" {
  name                  = "raw"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

module "postgresdb" {
  source = "./postgresdb"
  resource_group_name = azurerm_resource_group.hackathonresource.name
  location = azurerm_resource_group.hackathonresource.location
}

module "container_registry" {
  source = "./container_registry"
  location = azurerm_resource_group.hackathonresource.location
  resource_group_name = azurerm_resource_group.hackathonresource.name
}
