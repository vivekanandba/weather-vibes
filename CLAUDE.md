# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Weather Vibes is a theme-based weather discovery engine that translates NASA POWER climate data into intuitive "when" and "where" recommendations. Users select "vibes" (e.g., "Perfect Stargazing Night," "Ideal Beach Day") and the app provides location-based heatmaps or time-based calendars showing optimal conditions.

## Architecture

This is a **monorepo** with three main components:

### 1. Client (Next.js Frontend)
- **Location**: `client/`
- **Framework**: Next.js 15 with App Router, React 19, TypeScript
- **UI**: Chakra UI v3 + Tailwind CSS v4
- **State**: Zustand stores
- **Maps**: Leaflet (react-leaflet) for interactive mapping
- **API Client**: Axios with TanStack Query for data fetching

### 2. Server (FastAPI Backend)
- **Location**: `server/`
- **Framework**: FastAPI with Pydantic v2 for validation
- **Data Layer**: Reads pre-processed NASA POWER data (GeoTIFFs or JSON)
- **Core Logic**: Vibe Engine (`server/app/core/vibe_engine.py`) scores locations based on weather parameters
- **API Endpoints**:
  - `/api/where` - Find best locations for a vibe
  - `/api/when` - Find best times for a vibe at a location
  - `/api/advisor` - Get specialized recommendations (fashion, farming, mood)

### 3. Data Pipeline
- **Location**: `data/`
- **Purpose**: Fetch and preprocess NASA POWER API data
- **Key Scripts**:
  - `cron_job.py` - Batch download weather data for configured regions
  - `aggregate_points.py` - Aggregate point data into monthly summaries
- **Outputs**: `data/outputs/` contains raw JSON downloads organized by location

## Common Commands

### Client Development
```bash
cd client
npm install                  # Install dependencies
npm run dev                  # Start development server (http://localhost:3000)
npm run build                # Build for production
npm run start                # Start production server
npm run lint                 # Run ESLint
```

### Server Development
```bash
cd server
python -m venv venv          # Create virtual environment (first time only)
source venv/bin/activate     # Activate venv (Windows: venv\Scripts\activate)
pip install -r requirements.txt  # Install dependencies
python app/main.py           # Run development server (http://localhost:8000)
uvicorn app.main:app --reload  # Alternative: run with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000  # Production mode
```

### Data Pipeline
```bash
cd data
python cron_job.py 2000 2024 --area bangalore_core_point --output-format JSON --output-dir outputs/bangalore  # Download data
python aggregate_points.py --log-level INFO  # Aggregate monthly data
```

### Testing Backend API
```bash
# Visit interactive docs at http://localhost:8000/docs
curl http://localhost:8000/health  # Health check
curl http://localhost:8000/vibes   # List available vibes
```

## Key Architectural Concepts

### The Vibe Engine
The core scoring algorithm lives in `server/app/core/vibe_engine.py`. Vibes are configured in `server/config/vibe_dictionary.json` with:

**Standard Vibes**: Define weather parameters with scoring methods:
- `low_is_better`: Lower values = higher scores (e.g., cloud cover, precipitation)
- `high_is_better`: Higher values = higher scores (e.g., sunshine)
- `optimal_range`: Values within range get score 100 with gradual falloff (e.g., temperature 24-32°C)

**Advisors**: Special vibes that return structured recommendations instead of numeric scores (fashion, crop, mood). Logic is in `server/app/core/advisors/`.

### Data Flow
1. **Data Pipeline** downloads historical NASA POWER data and stores it in `data/outputs/`
2. **Backend** reads this cached data and scores it using Vibe Engine based on vibe definitions
3. **Frontend** displays results as interactive maps (Where), calendars (When), or recommendation cards (Advisors)

### State Management (Frontend)
Zustand stores in `client/src/stores/`:
- Manage selected vibe, location, time range
- Handle UI state (modals, loading states)
- Cache API responses

### API Integration
Client services (`client/src/services/`) use Axios to call FastAPI backend. All requests go through React Query for caching and loading state management.

## Important File Locations

### Configuration Files
- `server/config/vibe_dictionary.json` - All vibe definitions (parameters, weights, scoring methods)
- `data/config/parameters.yaml` - NASA POWER parameters configuration
- `data/config/areas.yaml` - Predefined areas of interest (locations)
- `client/src/config/` - Frontend configuration (vibes, theme)

### Core Logic
- `server/app/core/vibe_engine.py` - Main scoring engine
- `server/app/core/advisors/` - Advisor-specific logic
- `server/app/services/data_service.py` - Data loading and caching
- `server/app/services/scoring_service.py` - Scoring algorithms

### API Routes
- `server/app/api/routes/where.py` - Location-based queries
- `server/app/api/routes/when.py` - Time-based queries
- `server/app/api/routes/advisor.py` - Advisor recommendations

### Frontend Components
- `client/src/components/map/` - Map visualization components
- `client/src/components/features/` - Where, When, Advisors UI
- `client/src/components/vibe/` - Vibe selection components

## NASA POWER Data Parameters

The app uses these weather parameters from NASA POWER API:
- `T2M` - Temperature at 2m (°C)
- `PRECTOTCORR` - Precipitation (mm/day)
- `CLOUD_AMT` - Cloud amount (%)
- `RH2M` - Relative humidity at 2m (%)
- `WS2M` - Wind speed at 2m (m/s)
- `ALLSKY_SFC_SW_DWN` - Solar radiation (kW-hr/m²/day)

## Adding New Vibes

Edit `server/config/vibe_dictionary.json`:
```json
{
  "my_custom_vibe": {
    "name": "My Custom Vibe",
    "description": "Description of the vibe",
    "parameters": [
      {
        "id": "T2M",
        "weight": 0.5,
        "scoring": "optimal_range",
        "optimal_min": 20,
        "optimal_max": 25,
        "falloff_rate": 2.0
      }
    ]
  }
}
```

For advisors, set `"type": "advisor"` and specify `"logic": "your_rules"`, then implement the logic in `server/app/core/advisors/your_rules.py`.

## Development Workflow

1. **Backend changes**: Edit files in `server/app/`, server auto-reloads with uvicorn
2. **Frontend changes**: Edit files in `client/src/`, Next.js hot-reloads automatically
3. **New vibes**: Add to `vibe_dictionary.json`, restart backend
4. **New data**: Run `cron_job.py` to download, then restart backend to reload cache
5. **API contract changes**: Update Pydantic models in `server/app/models/`, TypeScript types in `client/src/types/`

## Common Patterns

### Backend: Adding a new endpoint
1. Create route in `server/app/api/routes/`
2. Define Pydantic request/response models in `server/app/models/`
3. Register route in `server/app/api/router.py`
4. Implement service logic in `server/app/services/`

### Frontend: Adding a new feature
1. Create Zustand store in `client/src/stores/` if needed
2. Create service in `client/src/services/` for API calls
3. Build UI components in `client/src/components/`
4. Add TypeScript types in `client/src/types/`

### Data Pipeline: Adding a new location
1. Add location to `data/config/areas.yaml`
2. Run `cron_job.py` with the new area name
3. Restart backend to load new data

## Team Responsibilities (Original Design)
- **Bhawesh**: Frontend lead, UI/UX, Mapbox integration, "When" feature
- **Vivek**: Backend lead, API architecture, "Where" feature
- **Kiran**: Data pipeline, "Advisors" feature

## Environment Variables

### Client (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
```

### Server (.env)
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
DATA_PATH=./data
CORS_ORIGINS=http://localhost:3000
API_PREFIX=/api
```

## Project Structure Summary

```
weather-vibes/
├── client/           # Next.js frontend
│   ├── src/
│   │   ├── app/      # Next.js app directory (pages, layouts)
│   │   ├── components/  # React components
│   │   ├── services/    # API client services
│   │   ├── stores/      # Zustand state management
│   │   ├── types/       # TypeScript types
│   │   └── config/      # Frontend configuration
│   └── package.json
├── server/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Vibe engine & advisors
│   │   ├── models/   # Pydantic models
│   │   ├── services/ # Business logic
│   │   └── main.py   # FastAPI app entry
│   ├── config/       # Vibe dictionary
│   └── requirements.txt
├── data/             # Data pipeline
│   ├── config/       # YAML configs for areas & parameters
│   ├── pipeline/     # Data fetching modules
│   ├── outputs/      # Downloaded NASA POWER data
│   └── cron_job.py   # Batch download script
└── docs/             # Project documentation
```
