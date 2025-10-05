# Frontend Deployment Guide - Azure Static Web Apps

This guide provides detailed instructions for deploying the Weather Vibes Next.js frontend to Azure Static Web Apps.

## 📋 Prerequisites

- Azure CLI installed and configured
- Node.js 18+ installed locally
- GitHub repository with your code
- Backend API deployed (for API integration)

## 🏗️ Architecture Overview

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   GitHub Actions    │    │   Azure Static      │    │   Azure CDN         │
│   (CI/CD Pipeline)  │◄───┤   Web Apps          │◄───┤   (Global CDN)     │
│                     │    │                     │    │                     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                          │
           │                          │
           ▼                          ▼
┌─────────────────────┐    ┌─────────────────────┐
│   Next.js Build     │    │   Static Files      │
│   (Static Export)   │    │   (HTML/CSS/JS)     │
└─────────────────────┘    └─────────────────────┘
```

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Frontend for Static Export

#### 1.1 Update Next.js Configuration

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
  // Disable server-side features for static export
  experimental: {
    esmExternals: false,
  },
};

export default nextConfig;
```

#### 1.2 Update Package.json Scripts

Update `client/package.json`:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "export": "next build && next export",
    "lint": "eslint"
  }
}
```

#### 1.3 Configure Environment Variables

Create `client/.env.production`:
```env
# Production API URL (replace with your actual backend URL)
NEXT_PUBLIC_API_BASE_URL=https://weather-vibes-api.azurecontainerapps.io

# Mapbox token (if using maps)
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
```

Create `client/.env.local` (for local development):
```env
# Local development API URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Mapbox token
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
```

#### 1.4 Update API Service Configuration

Ensure `client/src/services/api.ts` uses environment variables:
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed in the future
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;
```

### Step 2: Create GitHub Actions Workflow

#### 2.1 Create Workflow Directory
```bash
mkdir -p .github/workflows
```

#### 2.2 Create Azure Static Web Apps Workflow

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
          env_file_path: "/client/.env.production"
```

#### 2.3 Create Alternative Manual Build Workflow

Create `.github/workflows/build-frontend.yml`:
```yaml
name: Build Frontend

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: client/package-lock.json
      
      - name: Install dependencies
        run: |
          cd client
          npm ci
      
      - name: Build application
        run: |
          cd client
          npm run build
        env:
          NEXT_PUBLIC_API_BASE_URL: ${{ secrets.NEXT_PUBLIC_API_BASE_URL }}
          NEXT_PUBLIC_MAPBOX_TOKEN: ${{ secrets.NEXT_PUBLIC_MAPBOX_TOKEN }}
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: frontend-build
          path: client/out/
```

### Step 3: Deploy to Azure Static Web Apps

#### 3.1 Create Static Web App via Azure CLI

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
```

#### 3.2 Alternative: Create via Azure Portal

1. Go to Azure Portal
2. Search for "Static Web Apps"
3. Click "Create"
4. Fill in the details:
   - **Subscription**: Your subscription
   - **Resource Group**: weather-vibes-rg
   - **Name**: weather-vibes-app
   - **Plan Type**: Free
   - **Region**: Central US
   - **Source**: GitHub
   - **GitHub account**: Your account
   - **Organization**: Your organization
   - **Repository**: weather-vibes
   - **Branch**: main
   - **Build Presets**: Next.js
   - **App location**: /client
   - **API location**: (leave empty)
   - **Output location**: out

#### 3.3 Configure GitHub Secrets

After creating the Static Web App, you'll need to configure GitHub secrets:

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `AZURE_STATIC_WEB_APPS_API_TOKEN`: Get this from the Azure portal
   - `NEXT_PUBLIC_API_BASE_URL`: Your backend API URL
   - `NEXT_PUBLIC_MAPBOX_TOKEN`: Your Mapbox token (if using maps)

### Step 4: Configure Custom Domain (Optional)

#### 4.1 Add Custom Domain via Azure CLI
```bash
# Add custom domain
az staticwebapp hostname set \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --hostname yourdomain.com
```

#### 4.2 Configure DNS
1. Add a CNAME record pointing to your Static Web App URL
2. Verify domain ownership in Azure Portal
3. Configure SSL certificate

### Step 5: Configure Environment-Specific Settings

#### 5.1 Update Static Web App Configuration

Create `client/public/staticwebapp.config.json`:
```json
{
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["anonymous"]
    }
  ],
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/images/*.{png,jpg,jpeg,gif,svg}", "/css/*", "/js/*"]
  },
  "mimeTypes": {
    ".json": "application/json"
  },
  "globalHeaders": {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block"
  }
}
```

#### 5.2 Configure Build Settings

Create `client/staticwebapp.config.json`:
```json
{
  "buildCommand": "npm run build",
  "outputLocation": "out",
  "appLocation": "/client"
}
```

### Step 6: Test Deployment

#### 6.1 Get Application URL
```bash
# Get the Static Web App URL
az staticwebapp show \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --query defaultHostname -o tsv
```

#### 6.2 Test Application
1. Visit your Static Web App URL
2. Test all major features:
   - Map loading
   - API calls to backend
   - Vibe selection
   - Location search
   - Time period selection

#### 6.3 Test API Integration
```bash
# Test that frontend can reach backend
curl -H "Origin: https://YOUR_STATIC_WEB_APP_URL" \
     https://YOUR_BACKEND_URL/health
```

### Step 7: Configure Monitoring and Analytics

#### 7.1 Enable Application Insights
```bash
# Create Application Insights
az monitor app-insights component create \
  --app weather-vibes-frontend \
  --location eastus \
  --resource-group weather-vibes-rg

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app weather-vibes-frontend \
  --resource-group weather-vibes-rg \
  --query instrumentationKey -o tsv)
```

#### 7.2 Add Analytics to Frontend

Create `client/src/utils/analytics.ts`:
```typescript
// Simple analytics tracking
export const trackEvent = (eventName: string, properties?: Record<string, any>) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, properties);
  }
};

export const trackPageView = (pageName: string) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('config', 'GA_MEASUREMENT_ID', {
      page_title: pageName,
    });
  }
};
```

## 🔧 Configuration Options

### Build Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `app_location` | Source code location | `/client` |
| `output_location` | Build output directory | `out` |
| `build_command` | Build command | `npm run build` |
| `api_location` | API source location | (empty) |

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL | Yes |
| `NEXT_PUBLIC_MAPBOX_TOKEN` | Mapbox API token | Optional |

## 📊 Performance Optimization

### 1. Enable Compression
Static Web Apps automatically enable compression for static assets.

### 2. Configure Caching
```json
{
  "globalHeaders": {
    "Cache-Control": "public, max-age=31536000, immutable"
  }
}
```

### 3. Optimize Images
- Use Next.js Image component with `unoptimized={true}` for static export
- Compress images before deployment
- Use appropriate formats (WebP when possible)

### 4. Bundle Analysis
```bash
# Analyze bundle size
cd client
npm install -g @next/bundle-analyzer
ANALYZE=true npm run build
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**: Check Node.js version and dependencies
2. **API Connection Issues**: Verify CORS settings on backend
3. **Map Loading Issues**: Check Mapbox token configuration
4. **Routing Issues**: Ensure proper static export configuration

### Debug Commands

```bash
# Check Static Web App status
az staticwebapp show --name weather-vibes-app --resource-group weather-vibes-rg

# View deployment logs
az staticwebapp show --name weather-vibes-app --resource-group weather-vibes-rg --query properties.repositoryUrl

# Test build locally
cd client
npm run build
npm run start
```

### Build Debugging

```bash
# Test static export locally
cd client
npm run build
npx serve out
```

## 🔄 Updates and Maintenance

### Update Application
1. Push changes to main branch
2. GitHub Actions will automatically build and deploy
3. Monitor deployment status in GitHub Actions tab

### Manual Deployment
```bash
# Trigger manual deployment
az staticwebapp environment set \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --environment-name production
```

### Backup Configuration
```bash
# Export Static Web App configuration
az staticwebapp show \
  --name weather-vibes-app \
  --resource-group weather-vibes-rg \
  --query properties > staticwebapp-config.json
```

## 📈 Monitoring and Analytics

### 1. Built-in Analytics
- Azure Static Web Apps provides built-in analytics
- View in Azure Portal under your Static Web App

### 2. Custom Analytics
- Integrate Google Analytics or Application Insights
- Track user interactions and performance metrics

### 3. Performance Monitoring
- Monitor Core Web Vitals
- Track API response times
- Monitor error rates

This completes the frontend deployment guide. Your Next.js application should now be deployed to Azure Static Web Apps with automatic CI/CD from GitHub.
