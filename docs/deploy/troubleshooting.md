# Troubleshooting Guide

Common issues and solutions for Weather Vibes Azure deployment.

## 🚨 Backend Issues (Azure Container Apps)

### Container Fails to Start

**Symptoms:**
- Container app shows "Failed" status
- No logs available
- Health check fails

**Solutions:**
```bash
# Check container app status
az containerapp show --name weather-vibes-api --resource-group weather-vibes-rg

# View detailed logs
az containerapp logs show --name weather-vibes-api --resource-group weather-vibes-rg --follow

# Check if image exists in ACR
az acr repository list --name weathervibesacr
```

**Common Causes:**
1. **Missing dependencies**: Check if all Python packages are in requirements.txt
2. **Port configuration**: Ensure app listens on 0.0.0.0:8000
3. **Environment variables**: Verify all required env vars are set

### ⚠️ **CRITICAL: Docker Platform Mismatch**

**Problem**: Container built for ARM64 (Apple Silicon) but Azure requires AMD64
```bash
ERROR: no child with platform linux/amd64 in index weathervibesacr.azurecr.io/weather-vibes-api:latest
```

**Root Cause**: Docker buildx defaults to host architecture (ARM64 on Apple Silicon)

**Solution**: Force AMD64 platform build
```bash
# Build for AMD64 platform specifically
docker buildx build --platform linux/amd64 -t weathervibesacr.azurecr.io/weather-vibes-api:latest . --push

# Verify platform
docker buildx imagetools inspect weathervibesacr.azurecr.io/weather-vibes-api:latest
```

**Prevention**: Always use `--platform linux/amd64` for Azure deployments

### Data Loading Issues

**Symptoms:**
- API returns empty responses
- "No data available" errors
- Data service initialization fails

**Solutions:**
```bash
# Check if data files are uploaded to blob storage
az storage blob list --container-name climate-data --account-name weathervibesdata

# Verify storage connection string
az containerapp show --name weather-vibes-api --resource-group weather-vibes-rg --query properties.template.containers[0].env
```

**Debug Steps:**
1. Check Azure storage account access
2. Verify data download on container startup
3. Test data service initialization locally

### ⚠️ **CRITICAL: Symlink Data Directory Issue**

**Problem**: `/app/data` is a symlink but target directory doesn't exist
```bash
ERROR: [Errno 17] File exists: '/app/data'
```

**Root Cause**: Docker creates `/app/data` as symlink to `../data`, but target doesn't exist

**Solution**: Update Azure storage service to handle symlinks
```python
# In azure_storage.py
if Path(local_path).is_symlink():
    target_path = Path(local_path).resolve()
    target_path.mkdir(parents=True, exist_ok=True)
```

**Verification**:
```bash
# Test data directory creation
curl https://YOUR_API_URL/api/debug/create-data-dir

# Check data status
curl https://YOUR_API_URL/api/debug/data-status
```

### ⚠️ **CRITICAL: Azure Storage Authentication**

**Problem**: DefaultAzureCredential fails in container environment
```bash
ERROR: DefaultAzureCredential failed to retrieve a token from the included credentials
```

**Root Cause**: Container doesn't have managed identity configured

**Solution**: Prioritize connection string over managed identity
```python
# In azure_storage.py - try connection string first
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if connection_string:
    self.blob_service = BlobServiceClient.from_connection_string(connection_string)
else:
    # Fallback to managed identity
    self.blob_service = BlobServiceClient(account_url=..., credential=DefaultAzureCredential())
```

### CORS Errors

**Symptoms:**
- Frontend can't connect to backend
- Browser console shows CORS errors
- API calls fail with preflight errors

**Solutions:**
```bash
# Update CORS origins
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --set-env-vars \
    CORS_ORIGINS='["https://weather-vibes-app.azurestaticapps.net","http://localhost:3000"]'
```

**Test CORS:**
```bash
# Test CORS from command line
curl -H "Origin: https://weather-vibes-app.azurestaticapps.net" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://YOUR_API_URL/health
```

### Memory Issues

**Symptoms:**
- Container crashes with OOM errors
- Slow response times
- Data processing fails

**Solutions:**
```bash
# Increase memory allocation
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --memory 4.0Gi

# Check current resource usage
az containerapp show --name weather-vibes-api --resource-group weather-vibes-rg --query properties.template.containers[0].resources
```

## 🌐 Frontend Issues (Azure Static Web Apps)

### Build Failures

**Symptoms:**
- GitHub Actions build fails
- Static export doesn't work
- Missing files in output

**Solutions:**
1. **Check Node.js version**: Ensure using Node.js 18+
2. **Verify build command**: Should be `npm run build`
3. **Check output location**: Should be `out` directory

**Debug locally:**
```bash
cd client
npm run build
ls -la out/
```

### API Connection Issues

**Symptoms:**
- Frontend can't reach backend
- Network errors in browser console
- API calls timeout

**Solutions:**
1. **Check environment variables**:
   ```bash
   # Verify API URL is set correctly
   echo $NEXT_PUBLIC_API_BASE_URL
   ```

2. **Test API connectivity**:
   ```bash
   # Test from local machine
   curl https://YOUR_API_URL/health
   ```

3. **Check CORS configuration** on backend

### ⚠️ **CRITICAL: Frontend Environment Variables in Static Export**

**Problem**: `process.env` variables not available in static Next.js exports
```javascript
// This doesn't work in static export
const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL; // undefined
```

**Root Cause**: Static exports don't have access to build-time environment variables at runtime

**Solution**: Runtime environment detection
```typescript
// In api.ts - detect environment at runtime
const getApiBaseUrl = () => {
  // In production (static export), use hardcoded Azure backend
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
    return 'https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io';
  }
  // For local development
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
};
```

**Alternative Solution**: Use build-time environment variables in GitHub Actions
```yaml
# In .github/workflows/azure-static-web-apps.yml
- name: Build app
  run: |
    cd client
    npm run build
  env:
    NEXT_PUBLIC_API_BASE_URL: https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io
```

### Map Loading Issues

**Symptoms:**
- Maps don't load
- Mapbox errors in console
- Missing map tiles

**Solutions:**
1. **Check Mapbox token**:
   ```bash
   # Verify token is set
   echo $NEXT_PUBLIC_MAPBOX_TOKEN
   ```

2. **Update token in environment variables**
3. **Check Mapbox account usage limits**

### Routing Issues

**Symptoms:**
- 404 errors on page refresh
- Direct URL access fails
- Navigation doesn't work

**Solutions:**
1. **Check static export configuration**:
   ```typescript
   // next.config.ts
   const nextConfig: NextConfig = {
     output: 'export',
     trailingSlash: true,
     // ... other config
   };
   ```

2. **Configure fallback routes** in `staticwebapp.config.json`

## 💾 Storage Issues (Azure Blob Storage)

### Upload Failures

**Symptoms:**
- Data files not uploaded
- Upload commands fail
- Missing climate data

**Solutions:**
```bash
# Check storage account status
az storage account show --name weathervibesdata --resource-group weather-vibes-rg

# Verify container exists
az storage container list --account-name weathervibesdata

# Re-upload data
az storage blob upload-batch --destination climate-data --source ../data --account-name weathervibesdata
```

### Access Permission Issues

**Symptoms:**
- Container app can't access blob storage
- Authentication errors
- Data download fails

**Solutions:**
```bash
# Get storage account key
STORAGE_KEY=$(az storage account keys list --resource-group weather-vibes-rg --account-name weathervibesdata --query '[0].value' -o tsv)

# Update container app with connection string
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --set-env-vars \
    AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=weathervibesdata;AccountKey=$STORAGE_KEY;EndpointSuffix=core.windows.net"
```

## 🔧 General Debugging

### Check Resource Status

```bash
# List all resources
az resource list --resource-group weather-vibes-rg --output table

# Check resource health
az resource show --name weather-vibes-api --resource-group weather-vibes-rg --resource-type Microsoft.App/containerApps
```

### View Logs

```bash
# Container app logs
az containerapp logs show --name weather-vibes-api --resource-group weather-vibes-rg --follow

# Static web app logs (via GitHub Actions)
# Check GitHub Actions tab in your repository
```

### Test Connectivity

```bash
# Test backend health
curl https://YOUR_API_URL/health

# Test frontend
curl https://YOUR_STATIC_WEB_APP_URL

# Test API endpoints
curl https://YOUR_API_URL/vibes
```

## 🚀 Performance Issues

### Slow Response Times

**Symptoms:**
- API calls take >30 seconds
- Frontend loads slowly
- Data processing is slow

**Solutions:**
1. **Scale container app**:
   ```bash
   az containerapp update \
     --name weather-vibes-api \
     --resource-group weather-vibes-rg \
     --min-replicas 2 \
     --max-replicas 5
   ```

2. **Increase resources**:
   ```bash
   az containerapp update \
     --name weather-vibes-api \
     --resource-group weather-vibes-rg \
     --cpu 2.0 \
     --memory 4.0Gi
   ```

3. **Enable caching** for static assets

### Cold Start Issues

**Symptoms:**
- First request takes 30+ seconds
- Intermittent slow responses
- Timeout errors

**Solutions:**
1. **Set minimum replicas**:
   ```bash
   az containerapp update \
     --name weather-vibes-api \
     --resource-group weather-vibes-rg \
     --min-replicas 1
   ```

2. **Use always-on instances** (if available in your plan)

## 🔍 Monitoring and Alerts

### Set Up Monitoring

```bash
# Create Application Insights
az monitor app-insights component create \
  --app weather-vibes-monitoring \
  --location eastus \
  --resource-group weather-vibes-rg

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app weather-vibes-monitoring \
  --resource-group weather-vibes-rg \
  --query instrumentationKey -o tsv)
```

### Common Metrics to Monitor

1. **Container App Metrics**:
   - CPU usage
   - Memory usage
   - Request count
   - Response time

2. **Storage Metrics**:
   - Blob storage usage
   - Request count
   - Error rate

3. **Static Web App Metrics**:
   - Page views
   - Error rate
   - Response time

## 🆘 Emergency Recovery

### Complete Redeployment

```bash
# Delete and recreate everything
az group delete --name weather-vibes-rg --yes
az group create --name weather-vibes-rg --location eastus

# Follow deployment guide again
```

### Data Recovery

```bash
# Download data backup
az storage blob download-batch \
  --destination ./backup \
  --source climate-data \
  --account-name weathervibesdata

# Restore data
az storage blob upload-batch \
  --destination climate-data \
  --source ./backup \
  --account-name weathervibesdata
```

### Rollback Deployment

```bash
# Rollback to previous container image
az containerapp update \
  --name weather-vibes-api \
  --resource-group weather-vibes-rg \
  --image weathervibesacr.azurecr.io/weather-vibes-api:previous-tag
```

## 📞 Getting Help

### Azure Support

1. **Azure Portal**: Go to your resource → Help + Support
2. **Azure CLI**: Use `az feedback` command
3. **Documentation**: Check Azure documentation for your services

### Community Resources

1. **Stack Overflow**: Tag with `azure-container-apps`, `azure-static-web-apps`
2. **GitHub Issues**: Check your repository issues
3. **Azure Forums**: Microsoft Q&A for Azure

### Log Collection

```bash
# Collect all relevant logs
mkdir -p troubleshooting-logs
az containerapp logs show --name weather-vibes-api --resource-group weather-vibes-rg > troubleshooting-logs/container-logs.txt
az staticwebapp show --name weather-vibes-app --resource-group weather-vibes-rg > troubleshooting-logs/static-web-app-info.txt
az resource list --resource-group weather-vibes-rg > troubleshooting-logs/resources.txt
```

This troubleshooting guide should help you resolve most common deployment issues. For persistent problems, consider reaching out to Azure support or the community forums.
