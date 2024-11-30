output "app_service_name" {
  value = azurerm_app_service.app.name
}

output "app_service_url" {
  value = azurerm_app_service.app.default_site_hostname
}

