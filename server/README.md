# Weather Vibes API

FastAPI backend for the Weather Vibes application - a theme-based weather discovery engine.

## 🌟 Features

- **Where Endpoint** (`/api/where`): Find the best locations for a given vibe
- **When Endpoint** (`/api/when`): Find the best times for a given vibe at a location
- **Advisor Endpoints** (`/api/advisor`): Get specialized recommendations (fashion, farming, mood)

## 📋 Prerequisites

- Python 3.9+
- pip or conda
- GeoTIFF data files (processed by data pipeline)

## 🚀 Quick Start

### 1. Clone and Navigate

```bash
cd server
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file as needed:
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
DATA_PATH=./data
CORS_ORIGINS=http://localhost:3000
```

### 5. Run the Server

**Development mode:**
```bash
python app/main.py
```

**Production mode with uvicorn:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## 📚 API Documentation

### Base Endpoints

#### `GET /`
Root endpoint with API information.

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "vibes_loaded": 8,
  "data_path": "./data"
}
```

#### `GET /vibes`
List all available vibes and advisors.

**Response:**
```json
{
  "total": 8,
  "standard_vibes": [
    {
      "id": "stargazing",
      "name": "Perfect Stargazing Night",
      "description": "Clear skies with low humidity for optimal star viewing",
      "type": "standard"
    }
  ],
  "advisors": [
    {
      "id": "fashion_stylist",
      "name": "AI Fashion Stylist",
      "description": "Weather-appropriate outfit recommendations",
      "type": "advisor"
    }
  ]
}
```

### Main Endpoints

#### `POST /api/where`
Find best locations for a vibe within a radius.

**Request:**
```json
{
  "vibe": "stargazing",
  "month": 7,
  "center_lat": 12.9716,
  "center_lon": 77.5946,
  "radius_km": 100,
  "resolution": 5
}
```

**Response:**
```json
{
  "vibe": "stargazing",
  "month": 7,
  "scores": [
    {"lat": 12.97, "lon": 77.59, "score": 85.5},
    {"lat": 13.02, "lon": 77.64, "score": 78.2}
  ],
  "max_score": 95.2,
  "min_score": 45.1,
  "metadata": {
    "center": {"lat": 12.9716, "lon": 77.5946},
    "radius_km": 100,
    "num_points": 50
  }
}
```

#### `POST /api/when`
Find best months for a vibe at a location.

**Request:**
```json
{
  "vibe": "beach_day",
  "lat": 12.9716,
  "lon": 77.5946
}
```

**Response:**
```json
{
  "vibe": "beach_day",
  "location": {"lat": 12.9716, "lon": 77.5946},
  "monthly_scores": [
    {"month": 1, "month_name": "January", "score": 72.5},
    {"month": 2, "month_name": "February", "score": 78.3}
  ],
  "best_month": 3,
  "worst_month": 7,
  "metadata": {
    "num_months": 12
  }
}
```

#### `POST /api/advisor`
Get specialized recommendations from an advisor.

**Request:**
```json
{
  "advisor_type": "fashion",
  "lat": 12.9716,
  "lon": 77.5946,
  "month": 7,
  "additional_params": {}
}
```

**Response:**
```json
{
  "advisor_type": "fashion",
  "location": {"lat": 12.9716, "lon": 77.5946},
  "recommendations": [
    {
      "item": "Light Cotton T-Shirt",
      "icon": "👕",
      "description": "Stay cool in breathable fabrics"
    },
    {
      "item": "Sunglasses",
      "icon": "🕶️",
      "description": "Protect your eyes from bright sun"
    }
  ],
  "metadata": {
    "month": 7
  },
  "raw_data": {
    "T2M": 28.5,
    "PRECTOTCORR": 2.1
  }
}
```

## 🗂️ Project Structure

```
server/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Configuration settings
│   ├── models/
│   │   ├── requests.py              # Pydantic request models
│   │   └── responses.py             # Pydantic response models
│   ├── api/
│   │   ├── router.py                # Main API router
│   │   └── routes/
│   │       ├── where.py             # Where endpoint
│   │       ├── when.py              # When endpoint
│   │       └── advisor.py           # Advisor endpoint
│   ├── core/
│   │   ├── vibe_engine.py           # Core vibe scoring engine
│   │   └── advisors/
│   │       ├── fashion_rules.py     # Fashion advisor logic
│   │       ├── crop_advisor.py      # Crop advisor logic
│   │       └── mood_predictor.py    # Mood advisor logic
│   ├── services/
│   │   ├── data_service.py          # GeoTIFF data access
│   │   └── scoring_service.py       # Scoring algorithms
│   └── utils/
│       └── geospatial.py            # Geospatial utilities
├── config/
│   └── vibe_dictionary.json         # Vibe configurations
├── data/                            # GeoTIFF data files
├── requirements.txt
├── .env.example
└── README.md
```

## 🎨 Available Vibes

### Standard Vibes
1. **stargazing** - Perfect Stargazing Night
2. **beach_day** - Ideal Beach Day
3. **cozy_rain** - Cozy Rainy Day
4. **kite_flying** - Perfect Kite Flying Weather
5. **hiking** - Ideal Hiking Conditions

### Advisors
1. **fashion** - AI Fashion Stylist
2. **crop** - Crop & Farming Advisor
3. **mood** - Climate Mood Predictor

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `False` |
| `DATA_PATH` | Path to GeoTIFF data | `./data` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `API_PREFIX` | API route prefix | `/api` |

### Adding New Vibes

Edit `config/vibe_dictionary.json`:

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

#### Scoring Methods

1. **low_is_better**: Lower values get higher scores (e.g., cloud cover)
   ```json
   {
     "id": "CLOUD_AMT",
     "weight": 0.6,
     "scoring": "low_is_better",
     "min": 0,
     "max": 100
   }
   ```

2. **high_is_better**: Higher values get higher scores (e.g., sunshine)
   ```json
   {
     "id": "ALLSKY_SFC_SW_DWN",
     "weight": 0.4,
     "scoring": "high_is_better",
     "min": 0,
     "max": 10
   }
   ```

3. **optimal_range**: Values within range get score 100, with gradual falloff
   ```json
   {
     "id": "T2M",
     "weight": 0.4,
     "scoring": "optimal_range",
     "optimal_min": 24,
     "optimal_max": 32,
     "falloff_rate": 2
   }
   ```

## 🧪 Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# List vibes
curl http://localhost:8000/vibes

# Where endpoint
curl -X POST http://localhost:8000/api/where \
  -H "Content-Type: application/json" \
  -d '{
    "vibe": "stargazing",
    "month": 7,
    "center_lat": 12.9716,
    "center_lon": 77.5946,
    "radius_km": 50,
    "resolution": 5
  }'
```

### Using Interactive Docs

Visit http://localhost:8000/docs for a Swagger UI interface with built-in testing capabilities.

## 📊 Weather Parameters

The API uses NASA POWER data parameters:

| Parameter | Description | Unit |
|-----------|-------------|------|
| `T2M` | Temperature at 2m | °C |
| `PRECTOTCORR` | Precipitation | mm/day |
| `CLOUD_AMT` | Cloud amount | % |
| `RH2M` | Relative humidity at 2m | % |
| `WS2M` | Wind speed at 2m | m/s |
| `ALLSKY_SFC_SW_DWN` | Solar radiation | kW-hr/m²/day |

## 🐛 Troubleshooting

### Import Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

### CORS Issues
Add your frontend URL to `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## 🚢 Deployment

### Using Docker (Future)
```bash
docker build -t weather-vibes-api .
docker run -p 8000:8000 weather-vibes-api
```

### Using systemd (Linux)
Create `/etc/systemd/system/weather-vibes.service`:
```ini
[Unit]
Description=Weather Vibes API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/server
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📝 License

MIT

## 👥 Team

Team Vibe Finders - NASA Space Apps Challenge

---

For more information, visit the [project documentation](../docs/project.md).
# Test backend deployment
