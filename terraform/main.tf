resource "azurerm_resource_group" "hackathonresource" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  account_kind             = "StorageV2"
}


resource "azurerm_storage_container" "storagecontainer" {
  name                  = "raw"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}


// postgresql server

resource "azurerm_postgresql_flexible_server" "pgserver" {
  name                          = "postgress-schools"
  resource_group_name           = var.resource_group_name
  location                      = var.location
  version                       = "12"
  public_network_access_enabled = true
  administrator_login           = var.db_admin_login
  administrator_password        = var.db_admin_pass
  zone                          = "1"

  storage_mb   = 32768
  storage_tier = "P30"

  sku_name    = "GP_Standard_D4s_v3"
  create_mode = "Default"

  authentication {
    password_auth_enabled = true
  }

}

resource "azurerm_postgresql_flexible_server_database" "pgdb" {
  name      = "top_1000_schools"
  server_id = azurerm_postgresql_flexible_server.pgserver.id
  collation = "en_US.utf8"
  charset   = "utf8"

  # prevent the possibility of accidental data loss
  lifecycle {
    prevent_destroy = false
  }
}

