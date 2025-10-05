# Azure CLI Commands Cheatsheet

Quick reference for Azure CLI commands used in Weather Vibes deployment.

## 🔐 Authentication & Setup

```bash
# Login to Azure
az login

# Set default subscription
az account set --subscription "Your Subscription Name"

# Check current account
az account show

# List all subscriptions
az account list --output table
```

## 📁 Resource Group Management

```bash
# Create resource group
az group create --name weather-vibes-rg --location eastus

# List resource groups
az group list --output table

# Show resource group details
az group show --name weather-vibes-rg

# Delete resource group (⚠️ DESTRUCTIVE)
az group delete --name weather-vibes-rg --yes
```

## 🐳 Azure Container Registry (ACR)

```bash
# Create ACR
az acr create \
  --resource-group weather-vibes-rg \
  --name weathervibesacr \
  --sku Basic \
  --admin-enabled true

# Login to ACR
az acr login --name weathervibesacr

# List ACR repositories
az acr repository list --name weathervibesacr

# Build and push image
az acr build --registry weathervibesacr --image weather-vibes-api:latest server/

# List images
az acr repository list --name weathervibesacr

# Delete image
az acr repository delete --name weathervibesacr --image weather-vibes-api:latest
```

## 🚀 Azure Container Apps

```bash
# Create Container Apps environment
az containerapp env create \
  --name weather-vibes-env \
  --resource-group weather-vibes-rg \
  --location eastus

# Create container app
az containerapp create \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --environment weather-vibes-env \
  --image weathervibesacr.azurecr.io/weather-vibes-api:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2.0Gi

# Update container app
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --image weathervibesacr.azurecr.io/weather-vibes-api:latest

# Show container app details
az containerapp show --name weather-vibes-api --resource-group weather-vibes-rg

# List container apps
az containerapp list --resource-group weather-vibes-rg --output table

# Get container app URL
az containerapp show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --query properties.configuration.ingress.fqdn -o tsv

# View logs
az containerapp logs show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --follow

# Update environment variables
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --set-env-vars \
    CORS_ORIGINS='["https://weather-vibes-app.azurestaticapps.net"]' \
    DATA_PATH=/app/data

# Scale container app
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --min-replicas 2 \
  --max-replicas 10

# Delete container app
az containerapp delete --name weather-vibes-api --resource-group weather-vibes-rg --yes
```

## 💾 Azure Storage

```bash
# Create storage account
az storage account create \
  --name weathervibesdata \
  --resource-group weather-vibes-rg \
  --location eastus \
  --sku Standard_LRS

# Create container
az storage container create \
  --name climate-data \
  --account-name weathervibesdata

# List containers
az storage container list --account-name weathervibesdata --output table

# Upload files
az storage blob upload-batch \
  --destination climate-data \
  --source ../data \
  --account-name weathervibesdata

# List blobs
az storage blob list \
  --container-name climate-data \
  --account-name weathervibesdata \
  --output table

# Download files
az storage blob download-batch \
  --destination ./download \
  --source climate-data \
  --account-name weathervibesdata

# Get storage account key
az storage account keys list \
  --resource-group weather-vibes-rg \
  --account-name weathervibesdata \
  --query '[0].value' -o tsv

# Get connection string
az storage account show-connection-string \
  --name weathervibesdata \
  --resource-group weather-vibes-rg \
  --query connectionString -o tsv
```

## 🌐 Azure Static Web Apps

```bash
# Create Static Web App
az staticwebapp create \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --source https://github.com/yourusername/weather-vibes \
  --location "Central US" \
  --branch main \
  --app-location "/client" \
  --output-location "out" \
  --login-with-github

# Show Static Web App details
az staticwebapp show --name weather-vibes-app --resource-group weather-vibes-rg

# List Static Web Apps
az staticwebapp list --resource-group weather-vibes-rg --output table

# Get Static Web App URL
az staticwebapp show \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --query defaultHostname -o tsv

# Add custom domain
az staticwebapp hostname set \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --hostname yourdomain.com

# List domains
az staticwebapp hostname list \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg

# Delete Static Web App
az staticwebapp delete --name weather-vibes-app --resource-group weather-vibes-rg --yes
```

## 📊 Monitoring & Logs

```bash
# View container app logs
az containerapp logs show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --follow

# View recent logs
az containerapp logs show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --tail 100

# Check container app status
az containerapp show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --query properties.runningStatus

# List all resources in resource group
az resource list --resource-group weather-vibes-rg --output table

# Get resource costs
az consumption usage list \
  --billing-period-name "2024-01" \
  --resource-group weather-vibes-rg
```

## 🔧 Environment Variables

```bash
# Set environment variables for container app
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --set-env-vars \
    HOST=0.0.0.0 \
    PORT=8000 \
    DATA_PATH=/app/data \
    CORS_ORIGINS='["https://weather-vibes-app.azurestaticapps.net"]'

# Remove environment variable
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --remove-env-vars VARIABLE_NAME

# List environment variables
az containerapp show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --query properties.template.containers[0].env
```

## 🔍 Troubleshooting Commands

```bash
# Check container app health
az containerapp show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --query properties.runningStatus

# Get container app events
az containerapp revision list \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg

# Check storage account status
az storage account show \
  --name weathervibesdata \
  --resource-group weather-vibes-rg \
  --query provisioningState

# Test API endpoint
curl -I https://$(az containerapp show --name weather-vibes-api --resource-group weather-vibes-rg --query properties.configuration.ingress.fqdn -o tsv)/health

# Check Static Web App deployment status
az staticwebapp show \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --query properties.repositoryUrl
```

## 🧹 Cleanup Commands

```bash
# Delete all resources in resource group
az group delete --name weather-vibes-rg --yes

# Delete specific container app
az containerapp delete --name weather-vibes-api --resource-group weather-vibes-rg --yes

# Delete storage account
az storage account delete --name weathervibesdata --resource-group weather-vibes-rg --yes

# Delete ACR
az acr delete --name weathervibesacr --resource-group weather-vibes-rg --yes

# Delete Static Web App
az staticwebapp delete --name weather-vibes-app --resource-group weather-vibes-rg --yes
```

## 📋 Quick Deployment Script

Create `deploy.sh`:
```bash
#!/bin/bash

# Set variables
RESOURCE_GROUP="weather-vibes-rg"
LOCATION="eastus"
ACR_NAME="weathervibesacr"
CONTAINER_APP_NAME="weather-vibes-api"
STATIC_WEB_APP_NAME="weather-vibes-app"
STORAGE_ACCOUNT="weathervibesdata"

echo "🚀 Starting Weather Vibes deployment..."

# Create resource group
echo "📁 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create ACR
echo "🐳 Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Create Container Apps environment
echo "🚀 Creating Container Apps environment..."
az containerapp env create --name weather-vibes-env --resource-group $RESOURCE_GROUP --location $LOCATION

# Build and push image
echo "🔨 Building and pushing container image..."
az acr build --registry $ACR_NAME --image weather-vibes-api:latest server/

# Create storage account
echo "💾 Creating storage account..."
az storage account create --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --location $LOCATION --sku Standard_LRS
az storage container create --name climate-data --account-name $STORAGE_ACCOUNT

# Deploy container app
echo "🚀 Deploying container app..."
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment weather-vibes-env \
  --image $ACR_NAME.azurecr.io/weather-vibes-api:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2.0Gi

# Get URLs
echo "🔗 Getting deployment URLs..."
API_URL=$(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)
echo "✅ Backend API: https://$API_URL"

echo "🎉 Deployment completed!"
echo "Next steps:"
echo "1. Upload your data files to Azure Blob Storage"
echo "2. Deploy your frontend to Azure Static Web Apps"
echo "3. Configure CORS settings"
```

Make it executable:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📚 Additional Resources

- [Azure CLI Documentation](https://docs.microsoft.com/en-us/cli/azure/)
- [Azure Container Apps CLI Reference](https://docs.microsoft.com/en-us/cli/azure/containerapp)
- [Azure Static Web Apps CLI Reference](https://docs.microsoft.com/en-us/cli/azure/staticwebapp)
- [Azure Storage CLI Reference](https://docs.microsoft.com/en-us/cli/azure/storage)
