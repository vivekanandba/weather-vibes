# Comprehensive FastAPI Backend Implementation Plan for Weather Vibes

## Overview
This document outlines the complete implementation plan for building the FastAPI backend framework based on the Weather Vibes project requirements.

---

## Phase 1: Project Foundation & Structure

### 1.1 Directory Structure
```
server/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entry point
│   ├── config.py                    # Environment config & settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py              # Pydantic request models
│   │   └── responses.py             # Pydantic response models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py                # Main API router
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── where.py             # POST /api/where
│   │       ├── when.py              # POST /api/when
│   │       └── advisor.py           # POST /api/advisor
│   ├── core/
│   │   ├── __init__.py
│   │   ├── vibe_engine.py           # Core scoring algorithms
│   │   ├── vibe_dictionary.py       # Load & parse vibe configs
│   │   └── advisors/
│   │       ├── __init__.py
│   │       ├── fashion_rules.py     # Fashion stylist logic
│   │       ├── crop_advisor.py      # Farming advisor logic
│   │       └── mood_predictor.py    # Climate mood logic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_service.py          # GeoTIFF reading & caching
│   │   └── scoring_service.py       # Parameter scoring functions
│   └── utils/
│       ├── __init__.py
│       └── geospatial.py            # Coordinate/grid utilities
├── data/                            # Local GeoTIFF cache directory
├── config/
│   └── vibe_dictionary.json         # Vibe configurations
├── requirements.txt
├── .env.example
└── README.md
```

### 1.2 Core Configuration Files

#### requirements.txt
```
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
```

#### .env.example
```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Data Configuration
DATA_PATH=./data
GEOTIFF_CACHE_SIZE=100

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# API Configuration
API_PREFIX=/api
API_VERSION=v1
```

#### config.py Structure
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    data_path: str = "./data"
    cors_origins: List[str] = ["http://localhost:3000"]
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"
```

---

## Phase 2: Data Models & API Contracts

### 2.1 Request Models (app/models/requests.py)

#### WhereRequest
```python
from pydantic import BaseModel, Field
from typing import Optional

class WhereRequest(BaseModel):
    vibe: str = Field(..., description="Vibe ID (e.g., 'stargazing', 'beach_day')")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    year: Optional[int] = Field(None, description="Year for historical data")
    center_lat: float = Field(..., ge=-90, le=90, description="Center latitude")
    center_lon: float = Field(..., ge=-180, le=180, description="Center longitude")
    radius_km: float = Field(..., gt=0, le=500, description="Search radius in km")
    resolution: Optional[float] = Field(5, description="Grid resolution in km")
```

#### WhenRequest
```python
class WhenRequest(BaseModel):
    vibe: str = Field(..., description="Vibe ID")
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    year: Optional[int] = Field(None, description="Year for historical data")
```

#### AdvisorRequest
```python
class AdvisorRequest(BaseModel):
    advisor_type: str = Field(..., description="Type: 'fashion', 'crop', 'mood'")
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    month: int = Field(..., ge=1, le=12)
    year: Optional[int] = None
    additional_params: Optional[dict] = None
```

### 2.2 Response Models (app/models/responses.py)

#### WhereResponse
```python
from typing import List
from pydantic import BaseModel

class LocationScore(BaseModel):
    lat: float
    lon: float
    score: float

class WhereResponse(BaseModel):
    vibe: str
    month: int
    scores: List[LocationScore]
    max_score: float
    min_score: float
    metadata: dict
```

#### WhenResponse
```python
class MonthlyScore(BaseModel):
    month: int
    month_name: str
    score: float

class WhenResponse(BaseModel):
    vibe: str
    location: dict
    monthly_scores: List[MonthlyScore]
    best_month: int
    worst_month: int
    metadata: dict
```

#### AdvisorResponse
```python
class Recommendation(BaseModel):
    item: str
    icon: str
    description: Optional[str] = None

class AdvisorResponse(BaseModel):
    advisor_type: str
    location: dict
    recommendations: List[Recommendation]
    metadata: dict
    raw_data: Optional[dict] = None
```

---

## Phase 3: Core Vibe Engine Implementation

### 3.1 Vibe Dictionary (config/vibe_dictionary.json)

```json
{
  "stargazing": {
    "name": "Perfect Stargazing Night",
    "description": "Clear skies with low humidity for optimal star viewing",
    "parameters": [
      {
        "id": "CLOUD_AMT",
        "weight": 0.6,
        "scoring": "low_is_better",
        "min": 0,
        "max": 100
      },
      {
        "id": "RH2M",
        "weight": 0.4,
        "scoring": "low_is_better",
        "min": 0,
        "max": 100
      }
    ]
  },
  "beach_day": {
    "name": "Ideal Beach Day",
    "description": "Warm, sunny weather with minimal rain",
    "parameters": [
      {
        "id": "ALLSKY_SFC_SW_DWN",
        "weight": 0.4,
        "scoring": "high_is_better",
        "min": 0,
        "max": 10
      },
      {
        "id": "T2M",
        "weight": 0.4,
        "scoring": "optimal_range",
        "optimal_min": 24,
        "optimal_max": 32,
        "falloff_rate": 2
      },
      {
        "id": "PRECTOTCORR",
        "weight": 0.2,
        "scoring": "low_is_better",
        "min": 0,
        "max": 50
      }
    ]
  },
  "cozy_rain": {
    "name": "Cozy Rainy Day",
    "description": "Gentle rain with comfortable temperature",
    "parameters": [
      {
        "id": "PRECTOTCORR",
        "weight": 0.5,
        "scoring": "optimal_range",
        "optimal_min": 5,
        "optimal_max": 20,
        "falloff_rate": 1.5
      },
      {
        "id": "T2M",
        "weight": 0.3,
        "scoring": "optimal_range",
        "optimal_min": 18,
        "optimal_max": 25,
        "falloff_rate": 2
      },
      {
        "id": "WS2M",
        "weight": 0.2,
        "scoring": "low_is_better",
        "min": 0,
        "max": 20
      }
    ]
  },
  "fashion_stylist": {
    "name": "AI Fashion Stylist",
    "type": "advisor",
    "description": "Weather-appropriate outfit recommendations",
    "parameters": ["T2M", "ALLSKY_SFC_SW_DWN", "PRECTOTCORR", "WS2M"],
    "logic": "fashion_rules"
  },
  "crop_advisor": {
    "name": "Crop & Farming Advisor",
    "type": "advisor",
    "description": "Optimal conditions for crop growth",
    "parameters": ["T2M", "PRECTOTCORR", "T2M_MIN", "T2M_MAX", "RH2M"],
    "logic": "crop_rules"
  },
  "mood_predictor": {
    "name": "Climate Mood Predictor",
    "type": "advisor",
    "description": "Wellness suggestions based on weather",
    "parameters": ["T2M", "ALLSKY_SFC_SW_DWN", "PRECTOTCORR", "RH2M"],
    "logic": "mood_rules"
  }
}
```

### 3.2 Scoring Service (app/services/scoring_service.py)

#### Core Scoring Functions
```python
import numpy as np
from typing import Dict, List

def score_low_is_better(value: float, min_val: float, max_val: float) -> float:
    """
    Lower values get higher scores (e.g., cloud cover for stargazing).
    Returns a score from 0-100.
    """
    if max_val == min_val:
        return 100.0

    normalized = (value - min_val) / (max_val - min_val)
    normalized = np.clip(normalized, 0, 1)
    return (1 - normalized) * 100

def score_high_is_better(value: float, min_val: float, max_val: float) -> float:
    """
    Higher values get higher scores (e.g., sunshine for beach days).
    Returns a score from 0-100.
    """
    if max_val == min_val:
        return 100.0

    normalized = (value - min_val) / (max_val - min_val)
    normalized = np.clip(normalized, 0, 1)
    return normalized * 100

def score_optimal_range(
    value: float,
    optimal_min: float,
    optimal_max: float,
    falloff_rate: float = 2.0
) -> float:
    """
    Values within the optimal range get score 100.
    Values outside fall off gradually based on falloff_rate.
    Uses trapezoidal function for smooth scoring.
    """
    if optimal_min <= value <= optimal_max:
        return 100.0

    # Calculate distance from optimal range
    if value < optimal_min:
        distance = optimal_min - value
        range_width = optimal_max - optimal_min
    else:  # value > optimal_max
        distance = value - optimal_max
        range_width = optimal_max - optimal_min

    # Apply exponential falloff
    score = 100 * np.exp(-(distance / (range_width * falloff_rate)) ** 2)
    return max(0, score)

def calculate_weighted_score(
    parameter_scores: Dict[str, float],
    weights: Dict[str, float]
) -> float:
    """
    Calculates the weighted average of parameter scores.
    """
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0

    weighted_sum = sum(
        parameter_scores.get(param_id, 0) * weight
        for param_id, weight in weights.items()
    )

    return weighted_sum / total_weight
```

### 3.3 Vibe Engine (app/core/vibe_engine.py)

```python
import json
from pathlib import Path
from typing import Dict, Any, List
from app.services.scoring_service import (
    score_low_is_better,
    score_high_is_better,
    score_optimal_range,
    calculate_weighted_score
)

class VibeEngine:
    def __init__(self, config_path: str = "config/vibe_dictionary.json"):
        self.config_path = Path(config_path)
        self.vibes: Dict[str, Any] = {}
        self.load_vibes()

    def load_vibes(self):
        """Load vibe configurations from JSON file."""
        with open(self.config_path, 'r') as f:
            self.vibes = json.load(f)

    def get_vibe_config(self, vibe_id: str) -> Dict[str, Any]:
        """Get configuration for a specific vibe."""
        if vibe_id not in self.vibes:
            raise ValueError(f"Vibe '{vibe_id}' not found")
        return self.vibes[vibe_id]

    def get_required_parameters(self, vibe_id: str) -> List[str]:
        """Get list of required parameters for a vibe."""
        config = self.get_vibe_config(vibe_id)

        if config.get("type") == "advisor":
            return config["parameters"]

        return [param["id"] for param in config["parameters"]]

    def calculate_vibe_score(
        self,
        vibe_id: str,
        parameter_values: Dict[str, float]
    ) -> float:
        """
        Calculate the vibe score based on parameter values.
        Returns a score from 0-100.
        """
        config = self.get_vibe_config(vibe_id)

        if config.get("type") == "advisor":
            raise ValueError("Advisors use custom logic, not scoring")

        parameter_scores = {}
        weights = {}

        for param_config in config["parameters"]:
            param_id = param_config["id"]
            weight = param_config["weight"]
            scoring_method = param_config["scoring"]

            value = parameter_values.get(param_id)
            if value is None:
                continue

            # Score based on method
            if scoring_method == "low_is_better":
                score = score_low_is_better(
                    value,
                    param_config["min"],
                    param_config["max"]
                )
            elif scoring_method == "high_is_better":
                score = score_high_is_better(
                    value,
                    param_config["min"],
                    param_config["max"]
                )
            elif scoring_method == "optimal_range":
                score = score_optimal_range(
                    value,
                    param_config["optimal_min"],
                    param_config["optimal_max"],
                    param_config.get("falloff_rate", 2.0)
                )
            else:
                raise ValueError(f"Unknown scoring method: {scoring_method}")

            parameter_scores[param_id] = score
            weights[param_id] = weight

        return calculate_weighted_score(parameter_scores, weights)

    def list_vibes(self) -> List[Dict[str, str]]:
        """List all available vibes with their names and descriptions."""
        return [
            {
                "id": vibe_id,
                "name": config.get("name", vibe_id),
                "description": config.get("description", ""),
                "type": config.get("type", "standard")
            }
            for vibe_id, config in self.vibes.items()
        ]

# Global instance
vibe_engine = VibeEngine()
```

---

## Phase 4: Data Service Layer

### 4.1 Data Service (app/services/data_service.py)

```python
import rasterio
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
from functools import lru_cache
from app.config import settings

class DataService:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.cache: Dict[str, rasterio.DatasetReader] = {}

    def _get_geotiff_path(
        self,
        parameter_id: str,
        month: int,
        year: Optional[int] = None
    ) -> Path:
        """Construct path to GeoTIFF file."""
        # Assuming naming convention: {parameter_id}_{year}_{month:02d}.tif
        # Or for climatology: {parameter_id}_{month:02d}_climatology.tif
        if year:
            filename = f"{parameter_id}_{year}_{month:02d}.tif"
        else:
            filename = f"{parameter_id}_{month:02d}_climatology.tif"

        return self.data_path / filename

    @lru_cache(maxsize=100)
    def load_geotiff(
        self,
        parameter_id: str,
        month: int,
        year: Optional[int] = None
    ) -> rasterio.DatasetReader:
        """Load GeoTIFF file with caching."""
        path = self._get_geotiff_path(parameter_id, month, year)

        if not path.exists():
            raise FileNotFoundError(f"GeoTIFF not found: {path}")

        return rasterio.open(path)

    def get_value_at_point(
        self,
        parameter_id: str,
        lat: float,
        lon: float,
        month: int,
        year: Optional[int] = None
    ) -> Optional[float]:
        """Get parameter value at a specific point."""
        dataset = self.load_geotiff(parameter_id, month, year)

        # Convert lat/lon to pixel coordinates
        row, col = dataset.index(lon, lat)

        # Read value from dataset
        try:
            value = dataset.read(1)[row, col]

            # Handle nodata values
            if value == dataset.nodata:
                return None

            return float(value)
        except IndexError:
            return None

    def get_values_in_radius(
        self,
        parameter_id: str,
        center_lat: float,
        center_lon: float,
        radius_km: float,
        month: int,
        resolution_km: float = 5.0,
        year: Optional[int] = None
    ) -> List[Tuple[float, float, float]]:
        """
        Get parameter values for all points within a radius.
        Returns list of (lat, lon, value) tuples.
        """
        dataset = self.load_geotiff(parameter_id, month, year)

        # Generate grid of points
        from app.utils.geospatial import generate_grid_points
        grid_points = generate_grid_points(
            center_lat, center_lon, radius_km, resolution_km
        )

        results = []
        for lat, lon in grid_points:
            try:
                row, col = dataset.index(lon, lat)
                value = dataset.read(1)[row, col]

                if value != dataset.nodata:
                    results.append((lat, lon, float(value)))
            except IndexError:
                continue

        return results

    def get_monthly_values(
        self,
        parameter_id: str,
        lat: float,
        lon: float,
        year: Optional[int] = None
    ) -> Dict[int, float]:
        """Get parameter values for all 12 months at a location."""
        monthly_values = {}

        for month in range(1, 13):
            value = self.get_value_at_point(
                parameter_id, lat, lon, month, year
            )
            if value is not None:
                monthly_values[month] = value

        return monthly_values

    def get_all_parameters(
        self,
        parameter_ids: List[str],
        lat: float,
        lon: float,
        month: int,
        year: Optional[int] = None
    ) -> Dict[str, float]:
        """Get values for multiple parameters at a point."""
        result = {}

        for param_id in parameter_ids:
            value = self.get_value_at_point(param_id, lat, lon, month, year)
            if value is not None:
                result[param_id] = value

        return result

# Global instance
data_service = DataService(settings.data_path)
```

---

## Phase 5: API Endpoints Implementation

### 5.1 Where Endpoint (app/api/routes/where.py)

```python
from fastapi import APIRouter, HTTPException
from app.models.requests import WhereRequest
from app.models.responses import WhereResponse, LocationScore
from app.core.vibe_engine import vibe_engine
from app.services.data_service import data_service

router = APIRouter()

@router.post("/where", response_model=WhereResponse)
async def find_where(request: WhereRequest):
    """
    Find the best locations for a given vibe within a radius.
    Returns a heatmap of vibe scores.
    """
    try:
        # Get vibe configuration
        vibe_config = vibe_engine.get_vibe_config(request.vibe)
        required_params = vibe_engine.get_required_parameters(request.vibe)

        # Get values in radius for each parameter
        scores = []

        # First, collect all unique grid points across all parameters
        # (In practice, they should align, but this ensures consistency)
        first_param = required_params[0]
        grid_data = data_service.get_values_in_radius(
            first_param,
            request.center_lat,
            request.center_lon,
            request.radius_km,
            request.month,
            request.resolution,
            request.year
        )

        # For each grid point, get all parameter values and calculate score
        for lat, lon, _ in grid_data:
            parameter_values = data_service.get_all_parameters(
                required_params,
                lat,
                lon,
                request.month,
                request.year
            )

            # Skip if any required parameters are missing
            if len(parameter_values) != len(required_params):
                continue

            # Calculate vibe score
            score = vibe_engine.calculate_vibe_score(
                request.vibe,
                parameter_values
            )

            scores.append(LocationScore(lat=lat, lon=lon, score=score))

        if not scores:
            raise HTTPException(
                status_code=404,
                detail="No valid data found in the specified area"
            )

        # Calculate statistics
        score_values = [s.score for s in scores]
        max_score = max(score_values)
        min_score = min(score_values)

        return WhereResponse(
            vibe=request.vibe,
            month=request.month,
            scores=scores,
            max_score=max_score,
            min_score=min_score,
            metadata={
                "center": {"lat": request.center_lat, "lon": request.center_lon},
                "radius_km": request.radius_km,
                "resolution_km": request.resolution,
                "num_points": len(scores)
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
```

### 5.2 When Endpoint (app/api/routes/when.py)

```python
from fastapi import APIRouter, HTTPException
from app.models.requests import WhenRequest
from app.models.responses import WhenResponse, MonthlyScore
from app.core.vibe_engine import vibe_engine
from app.services.data_service import data_service
import calendar

router = APIRouter()

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

@router.post("/when", response_model=WhenResponse)
async def find_when(request: WhenRequest):
    """
    Find the best months for a given vibe at a location.
    Returns monthly vibe scores.
    """
    try:
        # Get vibe configuration
        vibe_config = vibe_engine.get_vibe_config(request.vibe)
        required_params = vibe_engine.get_required_parameters(request.vibe)

        monthly_scores = []

        # Calculate score for each month
        for month in range(1, 13):
            parameter_values = data_service.get_all_parameters(
                required_params,
                request.lat,
                request.lon,
                month,
                request.year
            )

            # Skip if any required parameters are missing
            if len(parameter_values) != len(required_params):
                continue

            # Calculate vibe score
            score = vibe_engine.calculate_vibe_score(
                request.vibe,
                parameter_values
            )

            monthly_scores.append(MonthlyScore(
                month=month,
                month_name=MONTH_NAMES[month - 1],
                score=score
            ))

        if not monthly_scores:
            raise HTTPException(
                status_code=404,
                detail="No valid data found for the specified location"
            )

        # Find best and worst months
        best_month = max(monthly_scores, key=lambda x: x.score).month
        worst_month = min(monthly_scores, key=lambda x: x.score).month

        return WhenResponse(
            vibe=request.vibe,
            location={"lat": request.lat, "lon": request.lon},
            monthly_scores=monthly_scores,
            best_month=best_month,
            worst_month=worst_month,
            metadata={
                "year": request.year,
                "num_months": len(monthly_scores)
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
```

### 5.3 Advisor Endpoint (app/api/routes/advisor.py)

```python
from fastapi import APIRouter, HTTPException
from app.models.requests import AdvisorRequest
from app.models.responses import AdvisorResponse
from app.core.vibe_engine import vibe_engine
from app.services.data_service import data_service
from app.core.advisors import fashion_rules, crop_advisor, mood_predictor

router = APIRouter()

ADVISOR_FUNCTIONS = {
    "fashion": fashion_rules.generate_recommendations,
    "crop": crop_advisor.generate_recommendations,
    "mood": mood_predictor.generate_recommendations
}

@router.post("/advisor", response_model=AdvisorResponse)
async def get_advisor_recommendations(request: AdvisorRequest):
    """
    Get specialized recommendations from an advisor.
    """
    try:
        # Validate advisor type
        if request.advisor_type not in ADVISOR_FUNCTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown advisor type: {request.advisor_type}"
            )

        # Get advisor configuration
        advisor_key = f"{request.advisor_type}_stylist" if request.advisor_type == "fashion" else f"{request.advisor_type}_advisor"

        if request.advisor_type == "mood":
            advisor_key = "mood_predictor"

        vibe_config = vibe_engine.get_vibe_config(advisor_key)
        required_params = vibe_config["parameters"]

        # Get parameter values
        parameter_values = data_service.get_all_parameters(
            required_params,
            request.lat,
            request.lon,
            request.month,
            request.year
        )

        if not parameter_values:
            raise HTTPException(
                status_code=404,
                detail="No data available for the specified location"
            )

        # Get advisor function and generate recommendations
        advisor_func = ADVISOR_FUNCTIONS[request.advisor_type]
        recommendations = advisor_func(
            parameter_values,
            request.additional_params or {}
        )

        return AdvisorResponse(
            advisor_type=request.advisor_type,
            location={"lat": request.lat, "lon": request.lon},
            recommendations=recommendations,
            metadata={
                "month": request.month,
                "year": request.year
            },
            raw_data=parameter_values
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
```

---

## Phase 6: Advisor Logic Implementation

### 6.1 Fashion Stylist (app/core/advisors/fashion_rules.py)

```python
from typing import Dict, List
from app.models.responses import Recommendation

def generate_recommendations(
    parameters: Dict[str, float],
    additional_params: Dict
) -> List[Recommendation]:
    """
    Generate fashion recommendations based on weather parameters.
    """
    recommendations = []

    temp = parameters.get("T2M", 20)  # Temperature in Celsius
    sunshine = parameters.get("ALLSKY_SFC_SW_DWN", 0)  # kW-hr/m^2/day
    precipitation = parameters.get("PRECTOTCORR", 0)  # mm/day
    wind_speed = parameters.get("WS2M", 0)  # m/s

    # Temperature-based recommendations
    if temp > 30:
        recommendations.append(Recommendation(
            item="Light Cotton T-Shirt",
            icon="👕",
            description="Stay cool in breathable fabrics"
        ))
        recommendations.append(Recommendation(
            item="Shorts",
            icon="🩳",
            description="Perfect for hot weather"
        ))
    elif temp > 25:
        recommendations.append(Recommendation(
            item="Linen Shirt",
            icon="👔",
            description="Breathable and stylish"
        ))
    elif temp > 18:
        recommendations.append(Recommendation(
            item="Light Sweater",
            icon="🧥",
            description="Comfortable for mild weather"
        ))
    elif temp > 10:
        recommendations.append(Recommendation(
            item="Jacket",
            icon="🧥",
            description="Stay warm in cooler temperatures"
        ))
    else:
        recommendations.append(Recommendation(
            item="Winter Coat",
            icon="🧥",
            description="Bundle up for cold weather"
        ))

    # Sun protection
    if sunshine > 5:
        recommendations.append(Recommendation(
            item="Sunglasses",
            icon="🕶️",
            description="Protect your eyes from bright sun"
        ))
        recommendations.append(Recommendation(
            item="Sun Hat",
            icon="🧢",
            description="Shield your face from UV rays"
        ))

    # Rain protection
    if precipitation > 5:
        recommendations.append(Recommendation(
            item="Waterproof Jacket",
            icon="🧥",
            description="Stay dry in rainy conditions"
        ))
        recommendations.append(Recommendation(
            item="Umbrella",
            icon="☔",
            description="Essential for rain protection"
        ))
    elif precipitation > 1:
        recommendations.append(Recommendation(
            item="Light Rain Jacket",
            icon="🧥",
            description="Protection from light showers"
        ))

    # Wind protection
    if wind_speed > 10:
        recommendations.append(Recommendation(
            item="Windbreaker",
            icon="🧥",
            description="Block strong winds"
        ))

    return recommendations
```

### 6.2 Crop Advisor (app/core/advisors/crop_advisor.py)

```python
from typing import Dict, List
from app.models.responses import Recommendation

def generate_recommendations(
    parameters: Dict[str, float],
    additional_params: Dict
) -> List[Recommendation]:
    """
    Generate crop and farming recommendations.
    """
    recommendations = []

    temp = parameters.get("T2M", 20)
    precipitation = parameters.get("PRECTOTCORR", 0)
    temp_min = parameters.get("T2M_MIN", temp - 5)
    temp_max = parameters.get("T2M_MAX", temp + 5)
    humidity = parameters.get("RH2M", 50)

    # Frost alert
    if temp_min < 2:
        recommendations.append(Recommendation(
            item="Frost Alert",
            icon="❄️",
            description=f"Risk of frost (min temp: {temp_min:.1f}°C). Protect sensitive crops."
        ))

    # Optimal planting conditions
    if 15 <= temp <= 25 and 20 <= precipitation <= 50:
        recommendations.append(Recommendation(
            item="Optimal Planting Window",
            icon="🌱",
            description="Excellent conditions for planting most crops"
        ))

    # Drought warning
    if precipitation < 5:
        recommendations.append(Recommendation(
            item="Drought Warning",
            icon="🏜️",
            description="Low rainfall. Consider irrigation."
        ))

    # Heavy rain warning
    if precipitation > 100:
        recommendations.append(Recommendation(
            item="Heavy Rain Alert",
            icon="🌧️",
            description="Excessive rainfall may cause waterlogging"
        ))

    # Heat stress warning
    if temp_max > 35:
        recommendations.append(Recommendation(
            item="Heat Stress Warning",
            icon="🌡️",
            description=f"High temperatures (max: {temp_max:.1f}°C). Ensure adequate irrigation."
        ))

    # Humidity-related recommendations
    if humidity > 80:
        recommendations.append(Recommendation(
            item="High Humidity Alert",
            icon="💧",
            description="Risk of fungal diseases. Monitor crops closely."
        ))

    # Crop-specific recommendations (if crop type provided)
    crop_type = additional_params.get("crop_type")
    if crop_type == "tomato":
        if 20 <= temp <= 26 and 40 <= humidity <= 70:
            recommendations.append(Recommendation(
                item="Ideal Tomato Conditions",
                icon="🍅",
                description="Perfect weather for tomato growth"
            ))

    return recommendations
```

### 6.3 Mood Predictor (app/core/advisors/mood_predictor.py)

```python
from typing import Dict, List
from app.models.responses import Recommendation

def generate_recommendations(
    parameters: Dict[str, float],
    additional_params: Dict
) -> List[Recommendation]:
    """
    Generate wellness recommendations based on weather mood.
    """
    recommendations = []

    temp = parameters.get("T2M", 20)
    sunshine = parameters.get("ALLSKY_SFC_SW_DWN", 0)
    precipitation = parameters.get("PRECTOTCORR", 0)
    humidity = parameters.get("RH2M", 50)

    # Determine weather mood
    if sunshine > 6 and temp > 20 and precipitation < 1:
        mood = "Energetic & Bright"
        recommendations.append(Recommendation(
            item="Outdoor Exercise",
            icon="🏃",
            description="Perfect day for outdoor activities and exercise"
        ))
        recommendations.append(Recommendation(
            item="Vitamin D Boost",
            icon="☀️",
            description="Great sunlight for natural vitamin D"
        ))
    elif precipitation > 10:
        mood = "Cozy & Reflective"
        recommendations.append(Recommendation(
            item="Indoor Activities",
            icon="📚",
            description="Ideal for reading, creative work, or meditation"
        ))
        recommendations.append(Recommendation(
            item="Warm Beverages",
            icon="☕",
            description="Perfect weather for hot tea or coffee"
        ))
    elif temp < 10:
        mood = "Crisp & Invigorating"
        recommendations.append(Recommendation(
            item="Brisk Walk",
            icon="🚶",
            description="Cool weather perfect for energizing walks"
        ))
        recommendations.append(Recommendation(
            item="Warm Layers",
            icon="🧣",
            description="Bundle up and enjoy the fresh air"
        ))
    elif sunshine < 3:
        mood = "Calm & Mellow"
        recommendations.append(Recommendation(
            item="Self-Care Time",
            icon="🧘",
            description="Overcast days are great for introspection"
        ))
        recommendations.append(Recommendation(
            item="Light Therapy",
            icon="💡",
            description="Consider bright indoor lighting"
        ))
    else:
        mood = "Balanced & Pleasant"
        recommendations.append(Recommendation(
            item="Balanced Activities",
            icon="⚖️",
            description="Mix of indoor and outdoor activities"
        ))

    # Add mood as first recommendation
    recommendations.insert(0, Recommendation(
        item=f"Weather Mood: {mood}",
        icon="🌈",
        description="Overall atmospheric feeling"
    ))

    # Humidity-based wellness tips
    if humidity > 80:
        recommendations.append(Recommendation(
            item="Stay Hydrated",
            icon="💧",
            description="High humidity can be draining"
        ))
    elif humidity < 30:
        recommendations.append(Recommendation(
            item="Moisturize",
            icon="🧴",
            description="Low humidity may dry out skin"
        ))

    return recommendations
```

---

## Phase 7: Main Application Setup

### 7.1 Main FastAPI App (app/main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.api.router import api_router
from app.core.vibe_engine import vibe_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup: Load vibe dictionary
    print("Loading vibe dictionary...")
    vibe_engine.load_vibes()
    print(f"Loaded {len(vibe_engine.vibes)} vibes")

    yield

    # Shutdown: Cleanup if needed
    print("Shutting down...")

app = FastAPI(
    title="Weather Vibes API",
    description="Theme-based weather discovery engine",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Weather Vibes API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "vibes_loaded": len(vibe_engine.vibes)
    }

@app.get("/vibes")
async def list_vibes():
    """List all available vibes."""
    return {
        "vibes": vibe_engine.list_vibes()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
```

### 7.2 API Router (app/api/router.py)

```python
from fastapi import APIRouter
from app.api.routes import where, when, advisor

api_router = APIRouter()

api_router.include_router(where.router, tags=["where"])
api_router.include_router(when.router, tags=["when"])
api_router.include_router(advisor.router, tags=["advisor"])
```

---

## Phase 8: Utilities & Helpers

### 8.1 Geospatial Utils (app/utils/geospatial.py)

```python
import math
from typing import List, Tuple

def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers
    r = 6371

    return c * r

def generate_grid_points(
    center_lat: float,
    center_lon: float,
    radius_km: float,
    resolution_km: float
) -> List[Tuple[float, float]]:
    """
    Generate a grid of points within a radius.
    Returns list of (lat, lon) tuples.
    """
    points = []

    # Convert km to approximate degrees
    # (rough approximation: 1 degree ≈ 111 km at equator)
    lat_deg_per_km = 1 / 111.0
    lon_deg_per_km = 1 / (111.0 * math.cos(math.radians(center_lat)))

    radius_lat = radius_km * lat_deg_per_km
    radius_lon = radius_km * lon_deg_per_km
    resolution_lat = resolution_km * lat_deg_per_km
    resolution_lon = resolution_km * lon_deg_per_km

    # Generate grid
    lat = center_lat - radius_lat
    while lat <= center_lat + radius_lat:
        lon = center_lon - radius_lon
        while lon <= center_lon + radius_lon:
            # Check if point is within radius
            distance = haversine_distance(center_lat, center_lon, lat, lon)
            if distance <= radius_km:
                points.append((lat, lon))
            lon += resolution_lon
        lat += resolution_lat

    return points

def lat_lon_to_pixel(
    lat: float,
    lon: float,
    geotransform: Tuple[float, ...]
) -> Tuple[int, int]:
    """
    Convert lat/lon to pixel coordinates using GeoTransform.

    GeoTransform format:
    (top_left_x, pixel_width, rotation_x, top_left_y, rotation_y, pixel_height)
    """
    origin_x = geotransform[0]
    pixel_width = geotransform[1]
    origin_y = geotransform[3]
    pixel_height = geotransform[5]

    # Calculate pixel coordinates
    col = int((lon - origin_x) / pixel_width)
    row = int((lat - origin_y) / pixel_height)

    return row, col
```

---

## Phase 9: Testing & Documentation

### 9.1 README.md

```markdown
# Weather Vibes API

FastAPI backend for the Weather Vibes application - a theme-based weather discovery engine.

## Features

- **Where Endpoint**: Find the best locations for a given vibe
- **When Endpoint**: Find the best times for a given vibe at a location
- **Advisor Endpoints**: Get specialized recommendations (fashion, farming, mood)

## Setup

### Prerequisites

- Python 3.9+
- GeoTIFF data files (processed by data pipeline)

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

5. Ensure data files are in the `data/` directory

### Running the Server

Development mode:
```bash
python app/main.py
```

Production mode with uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### GET /health
Health check endpoint.

### GET /vibes
List all available vibes.

### POST /api/where
Find best locations for a vibe.

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
    ...
  ],
  "max_score": 95.2,
  "min_score": 45.1,
  "metadata": {...}
}
```

### POST /api/when
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
    ...
  ],
  "best_month": 3,
  "worst_month": 7,
  "metadata": {...}
}
```

### POST /api/advisor
Get specialized recommendations.

**Request:**
```json
{
  "advisor_type": "fashion",
  "lat": 12.9716,
  "lon": 77.5946,
  "month": 7
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
    ...
  ],
  "metadata": {...}
}
```

## Project Structure

```
server/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models/              # Pydantic models
│   ├── api/                 # API routes
│   ├── core/                # Core business logic
│   ├── services/            # Data and scoring services
│   └── utils/               # Utilities
├── config/
│   └── vibe_dictionary.json # Vibe configurations
├── data/                    # GeoTIFF data files
└── requirements.txt
```

## Configuration

### Environment Variables

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: False)
- `DATA_PATH`: Path to GeoTIFF data files
- `CORS_ORIGINS`: Allowed CORS origins

### Adding New Vibes

Edit `config/vibe_dictionary.json` to add new vibes:

```json
{
  "my_vibe": {
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

## Development

### Adding a New Endpoint

1. Create route file in `app/api/routes/`
2. Define Pydantic models in `app/models/`
3. Implement business logic in `app/core/` or `app/services/`
4. Register route in `app/api/router.py`

### Adding a New Advisor

1. Create advisor file in `app/core/advisors/`
2. Implement `generate_recommendations()` function
3. Add advisor configuration to `vibe_dictionary.json`
4. Register in `app/api/routes/advisor.py`

## Testing

Run with test GeoTIFF data:
```bash
python app/main.py
```

Access API docs at: http://localhost:8000/docs

## License

MIT
```

---

## Implementation Checklist

### Phase 1: Foundation ✓
- [ ] Create directory structure
- [ ] Create `requirements.txt`
- [ ] Create `.env.example`
- [ ] Implement `config.py`

### Phase 2: Data Models ✓
- [ ] Create request models (`requests.py`)
- [ ] Create response models (`responses.py`)

### Phase 3: Core Engine ✓
- [ ] Create `vibe_dictionary.json`
- [ ] Implement scoring functions (`scoring_service.py`)
- [ ] Implement vibe engine (`vibe_engine.py`)

### Phase 4: Data Service ✓
- [ ] Implement `data_service.py`
- [ ] Add GeoTIFF reading functionality
- [ ] Implement caching

### Phase 5: API Endpoints ✓
- [ ] Implement `/api/where` endpoint
- [ ] Implement `/api/when` endpoint
- [ ] Implement `/api/advisor` endpoint

### Phase 6: Advisors ✓
- [ ] Implement fashion stylist
- [ ] Implement crop advisor
- [ ] Implement mood predictor

### Phase 7: Main App ✓
- [ ] Create `main.py`
- [ ] Configure CORS
- [ ] Add API router
- [ ] Add health check endpoint

### Phase 8: Utilities ✓
- [ ] Implement geospatial utilities
- [ ] Add distance calculations
- [ ] Add grid generation

### Phase 9: Documentation ✓
- [ ] Create README.md
- [ ] Add API documentation
- [ ] Add setup instructions
- [ ] Create example requests

---

## Next Steps After Implementation

1. **Test with sample data**: Create small test GeoTIFF files
2. **Frontend integration**: Work with Bhawesh to integrate endpoints
3. **Performance optimization**: Profile and optimize slow endpoints
4. **Error handling**: Add comprehensive error handling
5. **Logging**: Implement structured logging
6. **Deployment**: Prepare for cloud deployment

---

## Notes for Vivek (Backend Lead)

- Focus on getting the "shell" working first (main.py, config, basic routing)
- Mock endpoints can return dummy data initially
- Coordinate with Kiran on GeoTIFF file naming conventions
- Work with Bhawesh on CORS configuration for frontend
- Consider using Docker for easier deployment
- Add rate limiting for production
- Implement request validation thoroughly with Pydantic
