terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "location" {
  default = "eastus"
}

resource "azurerm_resource_group" "finops_rg" {
  name     = "finops-automation-rg"
  location = var.location
}

resource "azurerm_storage_account" "finops_sa" {
  name                     = "finopsstorageauto01"
  resource_group_name      = azurerm_resource_group.finops_rg.name
  location                 = azurerm_resource_group.finops_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "finops_plan" {
  name                = "finops-consumption-plan"
  resource_group_name = azurerm_resource_group.finops_rg.name
  location            = azurerm_resource_group.finops_rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "finops_function" {
  name                = "azure-finops-waste-cleaner-func"
  resource_group_name = azurerm_resource_group.finops_rg.name
  location            = azurerm_resource_group.finops_rg.location

  storage_account_name       = azurerm_storage_account.finops_sa.name
  storage_account_access_key = azurerm_storage_account.finops_sa.primary_access_key
  service_plan_id            = azurerm_service_plan.finops_plan.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  identity {
    type = "SystemAssigned"
  }
}

