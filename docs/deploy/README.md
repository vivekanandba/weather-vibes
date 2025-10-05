# Azure Deployment Guide for Weather Vibes

This directory contains comprehensive deployment documentation for deploying the Weather Vibes application to Azure.

## 📁 Documentation Structure

- **[Azure Deployment Plan](./azure-deployment-plan.md)** - Complete deployment strategy and overview
- **[Backend Deployment Guide](./backend-deployment.md)** - FastAPI backend deployment to Azure Container Apps
- **[Frontend Deployment Guide](./frontend-deployment.md)** - Next.js frontend deployment to Azure Static Web Apps
- **[Azure CLI Commands](./azure-commands.md)** - Quick reference for Azure CLI commands
- **[Troubleshooting Guide](./troubleshooting.md)** - Common issues and solutions

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

## 📞 Support

For deployment issues, refer to the [Troubleshooting Guide](./troubleshooting.md) or check the Azure documentation links above.
