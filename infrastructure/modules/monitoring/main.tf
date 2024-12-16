resource "azurerm_log_analytics_workspace" "main" {
  name                = "log-analytics"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name                       = "example-diagnostic"
  target_resource_id         = azurerm_app_service.main.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  
}