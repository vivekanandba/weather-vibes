# Azure Deployment Plan for Weather Vibes

## Overview
- **Backend**: FastAPI application → **Azure Container Apps** (equivalent to Google Cloud Run)
- **Frontend**: Next.js application → **Azure Static Web Apps** (equivalent to Google Cloud Storage + CDN)
- **Data**: NASA climate data files → **Azure Blob Storage**

## 🎯 Azure Services Mapping

| Component | Google Cloud | Azure Equivalent | Purpose |
|-----------|--------------|------------------|---------|
| Backend API | Cloud Run | **Azure Container Apps** | Serverless container hosting |
| Frontend | Cloud Storage + CDN | **Azure Static Web Apps** | Static site hosting with CDN |
| Data Storage | Cloud Storage | **Azure Blob Storage** | Climate data files |
| Container Registry | GCR | **Azure Container Registry** | Docker image storage |

## 📋 Pre-Deployment Checklist

### 1. Azure Prerequisites
- [ ] Azure subscription
- [ ] Azure CLI installed (`az --version`)
- [ ] Docker installed locally
- [ ] Node.js 18+ for frontend build

### 2. Data Preparation
Your application requires the `data/` directory with climate data files. This needs to be uploaded to Azure Blob Storage.

## 🚀 Step-by-Step Deployment Plan

### Phase 1: Backend Deployment (Azure Container Apps)

#### 1.1 Create Azure Resources
```bash
# Login to Azure
az login

# Create resource group
az group create --name weather-vibes-rg --location eastus

# Create Azure Container Registry
az acr create --resource-group weather-vibes-rg --name weathervibesacr --sku Basic

# Create Azure Container Apps environment
az containerapp env create \
  --name weather-vibes-env \
  --resource-group weather-vibes-rg \
  --location eastus
```

#### 1.2 Prepare Backend for Containerization

Create `server/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for geospatial libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV DATA_PATH=/app/data

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `server/.dockerignore`:
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/
```

#### 1.3 Build and Push Container
```bash
# Login to ACR
az acr login --name weathervibesacr

# Build and push image
az acr build --registry weathervibesacr --image weather-vibes-api:latest server/
```

#### 1.4 Deploy to Container Apps
```bash
# Create container app
az containerapp create \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --environment weather-vibes-env \
  --image weathervibesacr.azurecr.io/weather-vibes-api:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars DATA_PATH=/app/data \
  --cpu 1.0 \
  --memory 2.0Gi
```

### Phase 2: Data Storage Setup (Azure Blob Storage)

#### 2.1 Create Storage Account
```bash
# Create storage account
az storage account create \
  --name weathervibesdata \
  --resource-group weather-vibes-rg \
  --location eastus \
  --sku Standard_LRS

# Create container for data files
az storage container create \
  --name climate-data \
  --account-name weathervibesdata
```

#### 2.2 Upload Data Files
```bash
# Upload your data directory to blob storage
az storage blob upload-batch \
  --destination climate-data \
  --source ../data \
  --account-name weathervibesdata
```

#### 2.3 Configure Container App to Access Blob Storage
You'll need to modify your backend to download data from blob storage on startup or use Azure Files for persistent storage.

### Phase 3: Frontend Deployment (Azure Static Web Apps)

#### 3.1 Prepare Frontend for Static Export

Update `client/next.config.ts`:
```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export', // Enable static export
  trailingSlash: true,
  images: {
    unoptimized: true // Required for static export
  },
  webpack: (config) => {
    // Fix for mapbox-gl
    config.module.rules.push({
      test: /\.mjs$/,
      include: /node_modules/,
      type: 'javascript/auto',
    });
    return config;
  },
  // Transpile mapbox-gl for Next.js
  transpilePackages: ['mapbox-gl'],
};

export default nextConfig;
```

#### 3.2 Create GitHub Actions Workflow

Create `.github/workflows/azure-static-web-apps.yml`:
```yaml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/client"
          api_location: ""
          output_location: "out"
          skip_app_build: false
```

#### 3.3 Deploy Frontend
```bash
# Create Static Web App
az staticwebapp create \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --source https://github.com/yourusername/weather-vibes \
  --location "Central US" \
  --branch main \
  --app-location "/client" \
  --output-location "out"
```

### Phase 4: Configuration and Environment Variables

#### 4.1 Backend Environment Variables
Update your backend configuration to use Azure services:

```python
# server/app/config.py - Add Azure-specific settings
class Settings(BaseSettings):
    # ... existing settings ...
    
    # Azure Configuration
    azure_storage_account: str = ""
    azure_storage_key: str = ""
    azure_storage_container: str = "climate-data"
    
    # Data Configuration for Azure
    data_path: str = "/tmp/data"  # Local temp path for downloaded data
    
    # CORS Configuration for production
    cors_origins: List[str] = [
        "https://weather-vibes-app.azurestaticapps.net",  # Your static web app URL
        "http://localhost:3000"  # For local development
    ]
```

#### 4.2 Frontend Environment Variables
Create `client/.env.production`:
```env
NEXT_PUBLIC_API_BASE_URL=https://weather-vibes-api.azurecontainerapps.io
```

### Phase 5: Data Access Strategy

Since your backend needs access to the climate data files, you have two options:

#### Option A: Download on Startup (Recommended for Container Apps)
Modify your backend to download data from Azure Blob Storage on startup:

```python
# Add to server/app/services/azure_storage.py
import os
from azure.storage.blob import BlobServiceClient

class AzureDataDownloader:
    def __init__(self, account_name: str, account_key: str, container_name: str):
        self.blob_service = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=account_key
        )
        self.container_name = container_name
    
    def download_data(self, local_path: str):
        """Download all data files from blob storage to local path"""
        # Implementation to download files
        pass
```

#### Option B: Use Azure Files (For persistent storage)
Mount Azure Files as a volume in your container app.

## 🔧 Post-Deployment Configuration

### 1. Update CORS Settings
```bash
# Update container app with production CORS origins
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --set-env-vars CORS_ORIGINS='["https://weather-vibes-app.azurestaticapps.net"]'
```

### 2. Configure Custom Domains (Optional)
```bash
# Add custom domain to Static Web App
az staticwebapp hostname set \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --hostname yourdomain.com
```

### 3. Set up Monitoring
- Enable Application Insights for both frontend and backend
- Set up alerts for container app health
- Monitor blob storage usage

## 📊 Cost Estimation

| Service | Estimated Monthly Cost |
|---------|----------------------|
| Azure Container Apps (1 vCPU, 2GB RAM) | ~$30-50 |
| Azure Static Web Apps (Standard) | ~$9 |
| Azure Blob Storage (10GB) | ~$0.20 |
| Azure Container Registry | ~$5 |
| **Total** | **~$45-65/month** |

## 🚨 Important Considerations

1. **Data Size**: Your climate data files are substantial. Consider compression or data optimization.
2. **Cold Starts**: Container Apps may have cold start delays. Consider always-on instances for production.
3. **Security**: Implement proper authentication and API keys for production.
4. **Monitoring**: Set up comprehensive logging and monitoring.
5. **Backup**: Implement data backup strategies for your climate data.

## 🔄 Deployment Commands Summary

```bash
# 1. Create Azure resources
az group create --name weather-vibes-rg --location eastus
az acr create --resource-group weather-vibes-rg --name weathervibesacr --sku Basic
az containerapp env create --name weather-vibes-env --resource-group weather-vibes-rg --location eastus

# 2. Build and deploy backend
az acr build --registry weathervibesacr --image weather-vibes-api:latest server/
az containerapp create --name weather-vibes-api --resource-group weather-vibes-rg --environment weather-vibes-env --image weathervibesacr.azurecr.io/weather-vibes-api:latest --target-port 8000 --ingress external

# 3. Create storage and upload data
az storage account create --name weathervibesdata --resource-group weather-vibes-rg --location eastus --sku Standard_LRS
az storage container create --name climate-data --account-name weathervibesdata
az storage blob upload-batch --destination climate-data --source ../data --account-name weathervibesdata

# 4. Deploy frontend
az staticwebapp create --name weather-vibes-app --resource-group weather-vibes-rg --source https://github.com/yourusername/weather-vibes --location "Central US" --branch main --app-location "/client" --output-location "out"
```

This plan provides a production-ready deployment strategy that scales with your application needs while maintaining cost efficiency.
