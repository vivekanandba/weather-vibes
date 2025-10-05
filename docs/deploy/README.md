# Azure Deployment Guide for Weather Vibes

This directory contains comprehensive deployment documentation for deploying the Weather Vibes application to Azure.

## 📁 Documentation Structure

- **[Azure Deployment Plan](./azure-deployment-plan.md)** - Complete deployment strategy and overview
- **[Backend Deployment Guide](./backend-deployment.md)** - FastAPI backend deployment to Azure Container Apps
- **[Frontend Deployment Guide](./frontend-deployment.md)** - Next.js frontend deployment to Azure Static Web Apps
- **[Azure CLI Commands](./azure-commands.md)** - Quick reference for Azure CLI commands
- **[Troubleshooting Guide](./troubleshooting.md)** - Common issues and solutions

## 🎯 Live Application URLs

### Production Endpoints
- **Frontend**: https://victorious-forest-09f551a0f.1.azurestaticapps.net
- **Backend API**: https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io
- **API Documentation**: https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/docs

### Testing Endpoints for Judges

#### 🔍 **Health & Status Checks**
```bash
# API Health Check
curl https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/health

# Version Information
curl https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/version

# Available Vibes
curl https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/vibes
```

#### 🗺️ **Core API Endpoints**
```bash
# Find locations for stargazing in Bangalore area
curl -X POST https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/api/where \
  -H "Content-Type: application/json" \
  -d '{
    "vibe": "stargazing",
    "center_lat": 12.9716,
    "center_lon": 77.5946,
    "radius_km": 50,
    "month": 7,
    "year": 2023
  }'

# Find best time for hiking in Coorg
curl -X POST https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/api/when \
  -H "Content-Type: application/json" \
  -d '{
    "vibe": "hiking",
    "center_lat": 12.4200,
    "center_lon": 75.7400,
    "radius_km": 30,
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }'

# Get weather advisor recommendations
curl -X POST https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/api/advisor \
  -H "Content-Type: application/json" \
  -d '{
    "vibe": "beach_day",
    "location": "Goa",
    "date": "2023-07-15"
  }'
```

#### 🔧 **Debug Endpoints**
```bash
# Data Status Check
curl https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/api/debug/data-status

# Test Data Download
curl https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io/api/debug/test-data-download
```

## 🎯 Quick Start

1. **Prerequisites**: Ensure you have Azure CLI installed and are logged in
2. **Backend**: Follow the [Backend Deployment Guide](./backend-deployment.md) to deploy the FastAPI service
3. **Frontend**: Follow the [Frontend Deployment Guide](./frontend-deployment.md) to deploy the Next.js app
4. **Data**: Upload climate data to Azure Blob Storage as outlined in the main plan

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Azure Static  │    │  Azure Container │    │  Azure Blob     │
│   Web Apps      │◄───┤  Apps            │◄───┤  Storage        │
│   (Frontend)    │    │  (Backend API)   │    │  (Climate Data) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📋 Pre-Deployment Checklist

- [ ] Azure subscription active
- [ ] Azure CLI installed (`az --version`)
- [ ] Docker installed locally
- [ ] Node.js 18+ installed
- [ ] GitHub repository with your code
- [ ] Climate data files ready for upload

## 🚀 Deployment Phases

1. **Phase 1**: Backend deployment (Azure Container Apps)
2. **Phase 2**: Data storage setup (Azure Blob Storage)
3. **Phase 3**: Frontend deployment (Azure Static Web Apps)
4. **Phase 4**: Configuration and environment setup
5. **Phase 5**: Testing and monitoring

## ⚠️ Critical Issues Faced & Solutions

### 🔧 **Issue 1: Azure CLI Provider Registration**
**Problem**: Missing subscription registration for Microsoft.ContainerRegistry
```bash
ERROR: (MissingSubscriptionRegistration) The subscription is not registered to use namespace 'Microsoft.ContainerRegistry'
```
**Solution**: 
```bash
az provider register -n Microsoft.ContainerRegistry --wait
az provider register -n Microsoft.App --wait
az provider register -n Microsoft.Storage --wait
az provider register -n Microsoft.OperationalInsights --wait
```

### 🔧 **Issue 2: Docker Platform Mismatch**
**Problem**: Container built for ARM64 (Apple Silicon) but Azure requires AMD64
```bash
ERROR: no child with platform linux/amd64 in index
```
**Solution**: Force AMD64 platform build
```bash
docker buildx build --platform linux/amd64 -t weathervibesacr.azurecr.io/weather-vibes-api:latest . --push
```

### 🔧 **Issue 3: Azure Storage Authentication**
**Problem**: DefaultAzureCredential failing in container environment
```bash
ERROR: DefaultAzureCredential failed to retrieve a token
```
**Solution**: Prioritize connection string over managed identity
```python
# In azure_storage.py - try connection string first
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if connection_string:
    self.blob_service = BlobServiceClient.from_connection_string(connection_string)
```

### 🔧 **Issue 4: Symlink Directory Creation**
**Problem**: `/app/data` symlink target doesn't exist, causing data download failures
```bash
ERROR: [Errno 17] File exists: '/app/data'
```
**Solution**: Handle symlink resolution in Azure storage service
```python
# Create symlink target directory instead of the symlink itself
if Path(local_path).is_symlink():
    target_path = Path(local_path).resolve()
    target_path.mkdir(parents=True, exist_ok=True)
```

### 🔧 **Issue 5: Frontend Environment Variables**
**Problem**: `process.env` not available in static Next.js exports
**Solution**: Runtime environment detection
```typescript
const getApiBaseUrl = () => {
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
    return 'https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io';
  }
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
};
```

### 🔧 **Issue 6: CORS Configuration**
**Problem**: Backend CORS not accepting frontend origin
**Solution**: Proper environment variable format
```bash
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --set-env-vars \
    CORS_ORIGINS="http://localhost:3000,https://victorious-forest-09f551a0f.1.azurestaticapps.net"
```

## 💰 Cost Estimation

| Service | Monthly Cost |
|---------|-------------|
| Azure Container Apps | ~$30-50 |
| Azure Static Web Apps | ~$9 |
| Azure Blob Storage | ~$0.20 |
| Azure Container Registry | ~$5 |
| **Total** | **~$45-65** |

## 🔗 Useful Links

- [Azure Container Apps Documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
- [Azure Static Web Apps Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [Azure Blob Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Next.js Static Export](https://nextjs.org/docs/advanced-features/static-html-export)

## 🎯 Current Deployment Status

### ✅ **Successfully Deployed & Working**
- **Backend API**: Fully operational with 12 climate data locations
- **Frontend**: Static web app with dynamic API integration
- **Data Pipeline**: Azure Blob Storage with automatic data download
- **Version Tracking**: `/version` endpoint for deployment verification
- **Debug Tools**: Comprehensive debugging endpoints for troubleshooting

### 📊 **System Metrics**
- **Data Locations**: 12 (Bangalore, Coorg, Goa, Hampi, Kodaikanal, Munnar, Ooty, Pondicherry, Wayanad, Chikmagalur, Mysore, Bandipur)
- **Available Vibes**: 8 (stargazing, hiking, beach_day, cozy_rain, kite_flying)
- **API Response Time**: <2 seconds for location queries
- **Data Size**: ~50MB climate data from NASA POWER API

### 🔍 **For Judges - Quick Verification**
1. **Health Check**: Visit `/health` endpoint
2. **Version Check**: Visit `/version` endpoint  
3. **API Test**: Use the curl commands above to test core functionality
4. **Frontend Test**: Visit the live frontend URL and test the map interface
5. **Data Verification**: Check `/api/debug/data-status` to confirm data availability

### 🚀 **Key Features Demonstrated**
- **Real Climate Data**: NASA POWER API integration with 12 Indian locations
- **Geospatial Analysis**: Location-based weather vibe scoring
- **Interactive Maps**: Leaflet.js integration with weather overlays
- **Responsive Design**: Mobile-friendly interface
- **Cloud-Native**: Full Azure deployment with auto-scaling

## 📞 Support

For deployment issues, refer to the [Troubleshooting Guide](./troubleshooting.md) or check the Azure documentation links above.
