# Backend Deployment Guide - Azure Container Apps

This guide provides detailed instructions for deploying the Weather Vibes FastAPI backend to Azure Container Apps.

## 📋 Prerequisites

- Azure CLI installed and configured
- Docker installed locally
- Python 3.11+ (for local development)
- Access to your Azure subscription

## 🏗️ Architecture Overview

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Azure Container   │    │   Azure Container   │    │   Azure Blob       │
│   Registry (ACR)    │◄───┤   Apps Environment  │◄───┤   Storage          │
│                     │    │                     │    │   (Climate Data)   │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                          │
           │                          │
           ▼                          ▼
┌─────────────────────┐    ┌─────────────────────┐
│   Docker Image      │    │   FastAPI Backend   │
│   (weather-vibes-   │    │   (Container App)   │
│    api:latest)      │    │                     │
└─────────────────────┘    └─────────────────────┘
```

## 🚀 Step-by-Step Deployment

### Step 1: Create Azure Resources

#### 1.1 Login and Create Resource Group
```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name weather-vibes-rg \
  --location eastus
```

#### 1.2 Create Azure Container Registry
```bash
# Create ACR (replace with your unique name)
az acr create \
  --resource-group weather-vibes-rg \
  --name weathervibesacr \
  --sku Basic \
  --admin-enabled true
```

#### 1.3 Create Container Apps Environment
```bash
# Create Container Apps environment
az containerapp env create \
  --name weather-vibes-env \
  --resource-group weather-vibes-rg \
  --location eastus
```

### Step 2: Prepare Backend for Containerization

#### 2.1 Create Dockerfile

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

#### 2.2 Create .dockerignore

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
.DS_Store
*.md
tests/
```

#### 2.3 Update Requirements for Azure

Add Azure storage dependencies to `server/requirements.txt`:
```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
rasterio>=1.3.9
geopandas>=0.14.0
numpy>=1.24.0
shapely>=2.0.0
python-multipart>=0.0.6
pytest>=7.0.0
httpx>=0.24.0
pandas>=1.5.0
fiona>=1.8.0
pyproj>=3.4.0
# Azure dependencies
azure-storage-blob>=12.19.0
azure-identity>=1.15.0
```

### Step 3: Build and Push Container Image

#### 3.1 Login to ACR
```bash
# Login to Azure Container Registry
az acr login --name weathervibesacr
```

#### 3.2 Build and Push Image
```bash
# Build and push image to ACR
az acr build \
  --registry weathervibesacr \
  --image weather-vibes-api:latest \
  server/
```

### Step 4: Deploy to Container Apps

#### 4.1 Create Container App
```bash
# Create the container app
az containerapp create \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --environment weather-vibes-env \
  --image weathervibesacr.azurecr.io/weather-vibes-api:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2.0Gi \
  --min-replicas 1 \
  --max-replicas 3 \
  --env-vars \
    DATA_PATH=/app/data \
    HOST=0.0.0.0 \
    PORT=8000
```

#### 4.2 Configure CORS for Production
```bash
# Update CORS origins for production
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --set-env-vars \
    CORS_ORIGINS='["https://weather-vibes-app.azurestaticapps.net","http://localhost:3000"]'
```

### Step 5: Configure Data Access

#### 5.1 Create Storage Account
```bash
# Create storage account for climate data
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

#### 5.2 Upload Climate Data
```bash
# Upload data files to blob storage
az storage blob upload-batch \
  --destination climate-data \
  --source ../data \
  --account-name weathervibesdata
```

#### 5.3 Configure Azure Storage Access

Create `server/app/services/azure_storage.py`:
```python
import os
import tempfile
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import logging

logger = logging.getLogger(__name__)

class AzureDataService:
    """Service for downloading climate data from Azure Blob Storage."""
    
    def __init__(self, account_name: str, container_name: str):
        self.account_name = account_name
        self.container_name = container_name
        
        # Use managed identity or connection string
        try:
            # Try managed identity first
            self.blob_service = BlobServiceClient(
                account_url=f"https://{account_name}.blob.core.windows.net",
                credential=DefaultAzureCredential()
            )
        except Exception:
            # Fallback to connection string
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if connection_string:
                self.blob_service = BlobServiceClient.from_connection_string(connection_string)
            else:
                raise Exception("No Azure storage credentials found")
    
    def download_data(self, local_path: str):
        """Download all data files from blob storage."""
        logger.info(f"Downloading data to {local_path}")
        
        # Create local directory
        Path(local_path).mkdir(parents=True, exist_ok=True)
        
        # List and download all blobs
        container_client = self.blob_service.get_container_client(self.container_name)
        
        for blob in container_client.list_blobs():
            # Create local file path
            local_file_path = Path(local_path) / blob.name
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download blob
            with open(local_file_path, "wb") as download_file:
                download_file.write(container_client.download_blob(blob.name).readall())
            
            logger.info(f"Downloaded {blob.name}")
        
        logger.info("Data download completed")
```

#### 5.4 Update Main Application

Modify `server/app/main.py` to download data on startup:
```python
# Add to the lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # ... existing startup code ...
    
    # Download data from Azure Blob Storage
    logger.info("Downloading climate data from Azure Blob Storage...")
    try:
        from app.services.azure_storage import AzureDataService
        
        azure_data_service = AzureDataService(
            account_name=os.getenv("AZURE_STORAGE_ACCOUNT", "weathervibesdata"),
            container_name=os.getenv("AZURE_STORAGE_CONTAINER", "climate-data")
        )
        
        azure_data_service.download_data(settings.data_path)
        logger.info("✓ Climate data downloaded successfully")
    except Exception as e:
        logger.error(f"Failed to download climate data: {e}")
        # Continue without data for now - you might want to handle this differently
    
    # ... rest of startup code ...
```

### Step 6: Configure Environment Variables

#### 6.1 Update Container App with Azure Storage
```bash
# Get storage account key
STORAGE_KEY=$(az storage account keys list \
  --resource-group weather-vibes-rg \
  --account-name weathervibesdata \
  --query '[0].value' -o tsv)

# Update container app with storage configuration
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --set-env-vars \
    AZURE_STORAGE_ACCOUNT=weathervibesdata \
    AZURE_STORAGE_CONTAINER=climate-data \
    AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=weathervibesdata;AccountKey=$STORAGE_KEY;EndpointSuffix=core.windows.net"
```

### Step 7: Test Deployment

#### 7.1 Get Application URL
```bash
# Get the application URL
az containerapp show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --query properties.configuration.ingress.fqdn -o tsv
```

#### 7.2 Test Health Endpoint
```bash
# Test the health endpoint
curl https://YOUR_APP_URL/health
```

#### 7.3 Test API Endpoints
```bash
# Test the vibes endpoint
curl https://YOUR_APP_URL/vibes

# Test the API docs
curl https://YOUR_APP_URL/docs
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATA_PATH` | Local path for climate data | `/app/data` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:3000"]` |
| `AZURE_STORAGE_ACCOUNT` | Azure storage account name | - |
| `AZURE_STORAGE_CONTAINER` | Azure storage container name | `climate-data` |
| `AZURE_STORAGE_CONNECTION_STRING` | Azure storage connection string | - |

### Scaling Configuration

```bash
# Update scaling settings
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --min-replicas 2 \
  --max-replicas 10 \
  --cpu 2.0 \
  --memory 4.0Gi
```

## 📊 Monitoring and Logs

### View Logs
```bash
# View container logs
az containerapp logs show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --follow
```

### Monitor Performance
```bash
# Get container app status
az containerapp show \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --query properties.runningStatus
```

## 🚨 Troubleshooting

### Common Issues

1. **Container fails to start**: Check logs for missing dependencies
2. **Data not loading**: Verify Azure storage configuration
3. **CORS errors**: Update CORS_ORIGINS environment variable
4. **Memory issues**: Increase memory allocation

### Debug Commands

```bash
# Check container app status
az containerapp show --name weather-vibes-api --resource-group weather-vibes-rg

# View recent logs
az containerapp logs show --name weather-vibes-api --resource-group weather-vibes-rg --tail 100

# Check environment variables
az containerapp show --name weather-vibes-api --resource-group weather-vibes-rg --query properties.template.containers[0].env
```

## 🔄 Updates and Maintenance

### Update Application
```bash
# Rebuild and push new image
az acr build --registry weathervibesacr --image weather-vibes-api:latest server/

# Update container app
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --image weathervibesacr.azurecr.io/weather-vibes-api:latest
```

### Backup Data
```bash
# Create backup of blob storage
az storage blob download-batch \
  --destination ./backup \
  --source climate-data \
  --account-name weathervibesdata
```

This completes the backend deployment guide. The FastAPI application should now be running on Azure Container Apps with access to your climate data stored in Azure Blob Storage.
