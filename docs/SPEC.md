# Weather Vibes - Technical Specification

**Project:** Weather Vibes - Theme-Based Weather Discovery Engine  
**Team:** Vibe Finders  
**Version:** 1.0  
**Last Updated:** October 4, 2025

---

## Table of Contents

1. [Project Summary](#1-project-summary)
2. [Functional Requirements](#2-functional-requirements)
3. [API Specifications](#3-api-specifications)
4. [Data Specifications](#4-data-specifications)
5. [Frontend Specifications](#5-frontend-specifications)
6. [Backend Specifications](#6-backend-specifications)
7. [Integration Specifications](#7-integration-specifications)
8. [Performance Requirements](#8-performance-requirements)
9. [Security Requirements](#9-security-requirements)
10. [Testing Requirements](#10-testing-requirements)

---

## 1. Project Summary

### 1.1 Purpose
Weather Vibes is a theme-based weather discovery engine that translates user intentions (vibes) into concrete weather recommendations using NASA's historical climate data. The application answers two key questions:
1. **"Where should I go?"** - Given a vibe and time
2. **"When should I go?"** - Given a vibe and location

### 1.2 Scope
The application will provide:
- Interactive heatmap visualization for location-based recommendations
- Time-series calendar for temporal recommendations
- Specialized advisor features for specific use cases
- Historical climate data analysis from NASA POWER API

### 1.3 Target Users
- Travel planners and bloggers
- Event organizers
- Outdoor activity enthusiasts
- Farmers and agricultural professionals
- General public interested in weather-based planning

---

## 2. Functional Requirements

### 2.1 Feature 1: "Where" - Vibe Hotspot Finder

#### 2.1.1 User Stories
**US-W1:** As a user, I want to select a "vibe" so that I can find locations that match my desired weather conditions.

**US-W2:** As a user, I want to specify a time period (month/season) so that I can see where that vibe is best experienced.

**US-W3:** As a user, I want to see a heatmap visualization so that I can quickly identify the best locations.

**US-W4:** As a user, I want to filter results by geographical region so that I can narrow down my search.

**US-W5:** As a user, I want to click on a location to see detailed vibe scores so that I can make informed decisions.

#### 2.1.2 Acceptance Criteria
- User can select from at least 5 predefined vibes
- User can select any month or season
- Heatmap displays color-coded scores (0-100) across the map
- User can zoom and pan the map
- Clicking a location shows a detailed score breakdown
- Results load within 2 seconds

#### 2.1.3 Input Requirements
- **Vibe:** Required, dropdown/button selection
- **Month:** Required, dropdown (Jan-Dec) or season selector
- **Region (optional):** Bounding box or preset regions

#### 2.1.4 Output Requirements
- **Heatmap Data:** GeoJSON with scores for each grid cell
- **Top Locations:** List of top 10 locations with scores
- **Score Breakdown:** Parameter-wise contribution to total score

---

### 2.2 Feature 2: "When" - Vibe Calendar

#### 2.2.1 User Stories
**US-T1:** As a user, I want to select a location so that I can see when my desired vibe is available.

**US-T2:** As a user, I want to select a "vibe" so that I can see month-by-month scores for that location.

**US-T3:** As a user, I want to see a visual calendar/chart so that I can quickly identify the best months.

**US-T4:** As a user, I want to see historical trends so that I can understand year-over-year patterns.

**US-T5:** As a user, I want to compare multiple vibes so that I can find the best month for multiple activities.

#### 2.2.2 Acceptance Criteria
- User can search for and select any location within coverage area
- User can select from at least 5 predefined vibes
- Monthly scores (0-100) are displayed as a bar chart or calendar heatmap
- User can see historical data for at least 3 years
- User can compare up to 3 vibes simultaneously
- Results load within 2 seconds

#### 2.2.3 Input Requirements
- **Location:** Required, searchable text input with autocomplete
- **Vibe:** Required, dropdown/button selection
- **Year Range (optional):** Multi-select for historical comparison

#### 2.2.4 Output Requirements
- **Monthly Scores:** Array of 12 scores (one per month)
- **Best Months:** Top 3 months highlighted
- **Historical Comparison:** Year-over-year data visualization
- **Confidence Scores:** Data quality indicators

---

### 2.3 Feature 3: Specialized Aura Advisors

#### 2.3.1 Crop & Farming Advisor

**User Stories:**
- **US-A1:** As a farmer, I want to input my crop type so that I can get planting window recommendations.
- **US-A2:** As a farmer, I want to receive frost/drought alerts so that I can protect my crops.

**Acceptance Criteria:**
- Support for at least 5 common crops (tomatoes, rice, wheat, corn, potatoes)
- Planting window recommendations based on temperature and precipitation
- Risk alerts for extreme weather conditions
- Location-specific advice

**Input Requirements:**
- Location (lat/lon or place name)
- Crop type
- Planting date (optional)

**Output Requirements:**
- Optimal planting window (date range)
- Risk assessment (low/medium/high)
- Weather alerts (frost, drought, excessive rain)
- Historical success probability

#### 2.3.2 Climate Mood Predictor

**User Stories:**
- **US-A3:** As a user, I want to see how weather affects my mood so that I can plan wellness activities.
- **US-A4:** As a user, I want personalized wellness suggestions so that I can adapt to weather conditions.

**Acceptance Criteria:**
- Mood predictions based on temperature, sunlight, humidity
- Daily wellness suggestions (exercise, indoor activities, etc.)
- Trend visualization for the week ahead
- Personalization based on user preferences

**Input Requirements:**
- Location
- Date range
- Mood sensitivity preferences (optional)

**Output Requirements:**
- Mood score (0-100)
- Wellness recommendations
- Activity suggestions
- Weather-mood correlation insights

#### 2.3.3 AI Fashion Stylist

**User Stories:**
- **US-A5:** As a user, I want weather-appropriate outfit suggestions so that I can dress comfortably.
- **US-A6:** As a user, I want style recommendations so that I can look good in any weather.

**Acceptance Criteria:**
- Outfit suggestions based on temperature, precipitation, wind, and sun
- At least 3 outfit options per weather condition
- Accessory recommendations (umbrella, sunglasses, jacket)
- Style customization (casual, formal, sporty)

**Input Requirements:**
- Location
- Date
- Style preference (optional)
- Occasion (optional)

**Output Requirements:**
- Outfit recommendations with images/icons
- Accessory list
- Comfort score
- Weather justification

---

## 3. API Specifications

### 3.1 Base Configuration

**Base URL:** `https://api.weathervibes.com` (TBD)  
**Protocol:** HTTPS  
**Format:** JSON  
**Authentication:** API Key (optional for MVP)  
**Rate Limiting:** 100 requests/minute

### 3.2 Common Response Structure

#### Success Response
```json
{
  "success": true,
  "data": {},
  "metadata": {
    "timestamp": "2025-10-04T10:30:00Z",
    "version": "1.0",
    "processingTime": 1.2
  }
}
```

#### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  },
  "metadata": {
    "timestamp": "2025-10-04T10:30:00Z",
    "version": "1.0"
  }
}
```

---

### 3.3 Endpoint: GET /api/where

**Purpose:** Get location recommendations for a specific vibe and time period.

#### Request Parameters
```json
{
  "vibe": "stargazing",           // Required: Vibe ID
  "month": 7,                     // Required: Month (1-12)
  "region": {                     // Optional: Geographic bounds
    "lat_min": 8.0,
    "lat_max": 20.0,
    "lon_min": 72.0,
    "lon_max": 88.0
  },
  "resolution": "medium"          // Optional: low, medium, high
}
```

#### Response
```json
{
  "success": true,
  "data": {
    "vibe": {
      "id": "stargazing",
      "name": "Perfect Stargazing",
      "description": "Clear skies and low humidity"
    },
    "month": 7,
    "monthName": "July",
    "heatmap": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [77.5946, 12.9716]
          },
          "properties": {
            "score": 85,
            "location": "Bangalore, India",
            "breakdown": {
              "CLOUD_AMT": 20,
              "RH2M": 45
            }
          }
        }
      ]
    },
    "topLocations": [
      {
        "location": "Leh, Ladakh",
        "coordinates": [77.5771, 34.1526],
        "score": 95,
        "reason": "Extremely clear skies with minimal humidity"
      }
    ],
    "statistics": {
      "avgScore": 72,
      "maxScore": 95,
      "minScore": 45,
      "coverage": "100%"
    }
  },
  "metadata": {
    "timestamp": "2025-10-04T10:30:00Z",
    "processingTime": 1.5,
    "dataSource": "NASA POWER API",
    "dataYears": "2015-2024"
  }
}
```

---

### 3.4 Endpoint: GET /api/when

**Purpose:** Get temporal recommendations for a specific vibe and location.

#### Request Parameters
```json
{
  "vibe": "beach_day",            // Required: Vibe ID
  "location": {                   // Required: Location
    "lat": 12.9716,
    "lon": 77.5946
  },
  "years": [2020, 2021, 2022]    // Optional: Historical years
}
```

#### Response
```json
{
  "success": true,
  "data": {
    "vibe": {
      "id": "beach_day",
      "name": "Ideal Beach Day",
      "description": "Warm, sunny weather with minimal rain"
    },
    "location": {
      "name": "Bangalore, India",
      "coordinates": [77.5946, 12.9716]
    },
    "monthlyScores": [
      {
        "month": 1,
        "monthName": "January",
        "score": 75,
        "historicalAvg": 73,
        "confidence": 0.95,
        "breakdown": {
          "ALLSKY_SFC_SW_DWN": 85,
          "T2M": 72,
          "PRECTOTCORR": 68
        }
      }
    ],
    "bestMonths": [
      {
        "month": 3,
        "monthName": "March",
        "score": 88,
        "reason": "Optimal temperature and sunshine with low rainfall"
      }
    ],
    "yearlyComparison": [
      {
        "year": 2020,
        "scores": [75, 78, 88, ...]
      }
    ]
  },
  "metadata": {
    "timestamp": "2025-10-04T10:30:00Z",
    "processingTime": 0.8,
    "dataSource": "NASA POWER API",
    "dataYears": "2015-2024"
  }
}
```

---

### 3.5 Endpoint: POST /api/advisor

**Purpose:** Get specialized recommendations from advisor features.

#### Request Parameters
```json
{
  "advisorType": "farming",       // Required: farming, mood, fashion
  "location": {                   // Required: Location
    "lat": 12.9716,
    "lon": 77.5946
  },
  "parameters": {                 // Advisor-specific parameters
    "cropType": "tomato",
    "plantingDate": "2025-03-15"
  }
}
```

#### Response (Farming Advisor)
```json
{
  "success": true,
  "data": {
    "advisorType": "farming",
    "location": {
      "name": "Bangalore, India",
      "coordinates": [77.5946, 12.9716]
    },
    "recommendations": {
      "plantingWindow": {
        "start": "2025-03-10",
        "end": "2025-04-15",
        "confidence": 0.88
      },
      "riskAssessment": {
        "overall": "medium",
        "factors": [
          {
            "type": "frost",
            "risk": "low",
            "date": null
          },
          {
            "type": "drought",
            "risk": "medium",
            "date": "2025-06-01"
          }
        ]
      },
      "alerts": [
        {
          "type": "warning",
          "message": "Low rainfall expected in June. Consider irrigation.",
          "date": "2025-06-01"
        }
      ],
      "expectedConditions": {
        "avgTemperature": 28,
        "totalRainfall": 120,
        "sunnyDays": 85
      }
    }
  },
  "metadata": {
    "timestamp": "2025-10-04T10:30:00Z",
    "processingTime": 1.0
  }
}
```

#### Response (Fashion Stylist)
```json
{
  "success": true,
  "data": {
    "advisorType": "fashion",
    "location": {
      "name": "Bangalore, India",
      "coordinates": [77.5946, 12.9716]
    },
    "date": "2025-10-15",
    "weather": {
      "temperature": 28,
      "condition": "partly_cloudy",
      "precipitation": 0,
      "wind": 12
    },
    "recommendations": [
      {
        "outfit": "light_summer_dress",
        "items": ["Linen Shirt", "Cotton Pants", "Sneakers"],
        "accessories": ["Sunglasses", "Light Scarf"],
        "comfortScore": 92,
        "style": "casual",
        "reason": "Warm weather with good ventilation needed"
      }
    ]
  },
  "metadata": {
    "timestamp": "2025-10-04T10:30:00Z",
    "processingTime": 0.5
  }
}
```

---

### 3.6 Endpoint: GET /api/vibes

**Purpose:** List all available vibes with their configurations.

#### Response
```json
{
  "success": true,
  "data": {
    "vibes": [
      {
        "id": "stargazing",
        "name": "Perfect Stargazing",
        "description": "Clear, dark skies with minimal light pollution",
        "icon": "🌟",
        "category": "astronomy",
        "parameters": [
          {
            "id": "CLOUD_AMT",
            "name": "Cloud Coverage",
            "weight": 0.6,
            "scoring": "low_is_better"
          },
          {
            "id": "RH2M",
            "name": "Relative Humidity",
            "weight": 0.4,
            "scoring": "low_is_better"
          }
        ]
      },
      {
        "id": "beach_day",
        "name": "Ideal Beach Day",
        "description": "Warm, sunny weather perfect for the beach",
        "icon": "🏖️",
        "category": "outdoor",
        "parameters": [
          {
            "id": "ALLSKY_SFC_SW_DWN",
            "name": "Solar Radiation",
            "weight": 0.4,
            "scoring": "high_is_better"
          },
          {
            "id": "T2M",
            "name": "Temperature",
            "weight": 0.4,
            "scoring": "optimal_range",
            "range": [24, 32]
          },
          {
            "id": "PRECTOTCORR",
            "name": "Precipitation",
            "weight": 0.2,
            "scoring": "low_is_better"
          }
        ]
      }
    ]
  },
  "metadata": {
    "timestamp": "2025-10-04T10:30:00Z",
    "total": 5
  }
}
```

---

## 4. Data Specifications

### 4.1 NASA POWER API Integration

#### 4.1.1 API Details
- **Base URL:** `https://power.larc.nasa.gov/api/temporal/climatology/`
- **Authentication:** None required
- **Data Format:** JSON, CSV
- **Coverage:** Global, 0.5° x 0.5° grid
- **Temporal Range:** 1984-present

#### 4.1.2 Required Parameters

| Parameter ID | Name | Unit | Description | Usage |
|--------------|------|------|-------------|-------|
| T2M | Temperature at 2m | °C | Air temperature | All vibes |
| PRECTOTCORR | Precipitation | mm/day | Total rainfall | Beach, farming |
| ALLSKY_SFC_SW_DWN | Solar Radiation | kWh/m²/day | Incoming sunlight | Beach, mood |
| RH2M | Relative Humidity | % | Moisture in air | Stargazing, comfort |
| WS2M | Wind Speed | m/s | Wind at 2m height | Fashion, outdoor |
| CLOUD_AMT | Cloud Coverage | % | Sky cloud cover | Stargazing, solar |
| T2M_MIN | Min Temperature | °C | Daily minimum | Farming (frost) |
| T2M_MAX | Max Temperature | °C | Daily maximum | Heat advisories |
| PS | Surface Pressure | kPa | Atmospheric pressure | Weather patterns |
| QV2M | Specific Humidity | g/kg | Absolute humidity | Comfort index |

#### 4.1.3 Data Fetching Strategy

**Batch Download:**
```python
# Pseudocode for data fetching
for vibe in vibes:
    for parameter in vibe.parameters:
        for month in range(1, 13):
            url = f"https://power.larc.nasa.gov/api/temporal/climatology/point"
            params = {
                "parameters": parameter.id,
                "community": "RE",
                "longitude": lon,
                "latitude": lat,
                "format": "JSON"
            }
            data = fetch(url, params)
            save_to_geotiff(data, vibe, parameter, month)
```

---

### 4.2 GeoTIFF File Structure

#### 4.2.1 File Naming Convention
```
{vibe_id}_{parameter_id}_{month}_{year_range}.tif

Examples:
- stargazing_CLOUD_AMT_07_2015-2024.tif
- beach_day_T2M_12_2015-2024.tif
```

#### 4.2.2 File Metadata
```json
{
  "vibe": "stargazing",
  "parameter": "CLOUD_AMT",
  "month": 7,
  "year_range": "2015-2024",
  "bounds": {
    "north": 35.0,
    "south": 8.0,
    "east": 88.0,
    "west": 68.0
  },
  "resolution": 0.5,
  "crs": "EPSG:4326",
  "units": "%",
  "data_source": "NASA POWER API",
  "processing_date": "2025-10-04"
}
```

#### 4.2.3 Storage Structure
```
data/
├── geotiffs/
│   ├── stargazing/
│   │   ├── CLOUD_AMT_01.tif
│   │   ├── CLOUD_AMT_02.tif
│   │   └── ...
│   ├── beach_day/
│   │   ├── T2M_01.tif
│   │   ├── ALLSKY_SFC_SW_DWN_01.tif
│   │   └── ...
│   └── ...
├── processed/
│   ├── stargazing_heatmap_01.geojson
│   └── ...
└── cache/
    ├── query_cache.db
    └── ...
```

---

### 4.3 Vibe Dictionary Specification

#### 4.3.1 Core Vibes

**1. Perfect Stargazing**
```json
{
  "id": "stargazing",
  "name": "Perfect Stargazing",
  "description": "Crystal clear skies with minimal light pollution",
  "icon": "🌟",
  "category": "astronomy",
  "parameters": [
    {
      "id": "CLOUD_AMT",
      "weight": 0.6,
      "scoring": "low_is_better",
      "optimal": {"min": 0, "max": 20}
    },
    {
      "id": "RH2M",
      "weight": 0.4,
      "scoring": "low_is_better",
      "optimal": {"min": 0, "max": 40}
    }
  ]
}
```

**2. Ideal Beach Day**
```json
{
  "id": "beach_day",
  "name": "Ideal Beach Day",
  "description": "Warm, sunny weather perfect for the beach",
  "icon": "🏖️",
  "category": "outdoor",
  "parameters": [
    {
      "id": "ALLSKY_SFC_SW_DWN",
      "weight": 0.4,
      "scoring": "high_is_better",
      "optimal": {"min": 5, "max": 8}
    },
    {
      "id": "T2M",
      "weight": 0.4,
      "scoring": "optimal_range",
      "range": [24, 32]
    },
    {
      "id": "PRECTOTCORR",
      "weight": 0.2,
      "scoring": "low_is_better",
      "optimal": {"min": 0, "max": 2}
    }
  ]
}
```

**3. Cozy Rainy Day**
```json
{
  "id": "rainy_day",
  "name": "Cozy Rainy Day",
  "description": "Perfect indoor weather with gentle rain",
  "icon": "🌧️",
  "category": "indoor",
  "parameters": [
    {
      "id": "PRECTOTCORR",
      "weight": 0.6,
      "scoring": "optimal_range",
      "range": [5, 20]
    },
    {
      "id": "T2M",
      "weight": 0.3,
      "scoring": "optimal_range",
      "range": [18, 24]
    },
    {
      "id": "CLOUD_AMT",
      "weight": 0.1,
      "scoring": "high_is_better"
    }
  ]
}
```

**4. Perfect Hiking Weather**
```json
{
  "id": "hiking",
  "name": "Perfect Hiking Weather",
  "description": "Comfortable temperature with clear trails",
  "icon": "🥾",
  "category": "outdoor",
  "parameters": [
    {
      "id": "T2M",
      "weight": 0.5,
      "scoring": "optimal_range",
      "range": [15, 25]
    },
    {
      "id": "PRECTOTCORR",
      "weight": 0.3,
      "scoring": "low_is_better",
      "optimal": {"min": 0, "max": 3}
    },
    {
      "id": "WS2M",
      "weight": 0.2,
      "scoring": "optimal_range",
      "range": [0, 5]
    }
  ]
}
```

**5. Kite Flying Paradise**
```json
{
  "id": "kite_flying",
  "name": "Kite Flying Paradise",
  "description": "Perfect wind conditions for kite flying",
  "icon": "🪁",
  "category": "outdoor",
  "parameters": [
    {
      "id": "WS2M",
      "weight": 0.6,
      "scoring": "optimal_range",
      "range": [3, 8]
    },
    {
      "id": "PRECTOTCORR",
      "weight": 0.2,
      "scoring": "low_is_better"
    },
    {
      "id": "CLOUD_AMT",
      "weight": 0.2,
      "scoring": "low_is_better"
    }
  ]
}
```

---

### 4.4 Scoring Algorithm Specification

#### 4.4.1 Low is Better
```python
def score_low_is_better(value, min_val, max_val):
    """
    Score where lower values are better (e.g., cloud coverage, humidity)
    Returns: Score from 0-100
    """
    if value <= min_val:
        return 100
    if value >= max_val:
        return 0
    
    normalized = (value - min_val) / (max_val - min_val)
    score = (1 - normalized) * 100
    return round(score, 2)
```

#### 4.4.2 High is Better
```python
def score_high_is_better(value, min_val, max_val):
    """
    Score where higher values are better (e.g., solar radiation)
    Returns: Score from 0-100
    """
    if value >= max_val:
        return 100
    if value <= min_val:
        return 0
    
    normalized = (value - min_val) / (max_val - min_val)
    score = normalized * 100
    return round(score, 2)
```

#### 4.4.3 Optimal Range
```python
def score_optimal_range(value, optimal_min, optimal_max, falloff_rate=0.1):
    """
    Score where values within a range are best (e.g., temperature)
    Returns: Score from 0-100
    """
    if optimal_min <= value <= optimal_max:
        return 100
    
    # Calculate distance from optimal range
    if value < optimal_min:
        distance = optimal_min - value
    else:
        distance = value - optimal_max
    
    # Apply exponential falloff
    score = 100 * math.exp(-falloff_rate * distance)
    return max(0, round(score, 2))
```

#### 4.4.4 Weighted Final Score
```python
def calculate_vibe_score(parameter_scores, weights):
    """
    Calculate final vibe score using weighted average
    Returns: Score from 0-100
    """
    total_weight = sum(weights.values())
    weighted_sum = sum(
        score * weights[param] 
        for param, score in parameter_scores.items()
    )
    
    final_score = weighted_sum / total_weight
    return round(final_score, 2)
```

---

## 5. Frontend Specifications

### 5.1 Technology Stack
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **UI Library:** Chakra UI
- **State Management:** Zustand
- **Map Library:** Mapbox GL JS with react-map-gl
- **Charts:** Recharts or Chart.js
- **HTTP Client:** Axios
- **Build Tool:** Turbopack (Next.js default)

### 5.2 Project Structure
```
client/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── where/
│   │   └── page.tsx
│   ├── when/
│   │   └── page.tsx
│   └── advisors/
│       └── page.tsx
├── components/
│   ├── common/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Layout.tsx
│   ├── where/
│   │   ├── VibeSelector.tsx
│   │   ├── HeatmapView.tsx
│   │   ├── LocationResults.tsx
│   │   └── FilterPanel.tsx
│   ├── when/
│   │   ├── LocationPicker.tsx
│   │   ├── VibeSelector.tsx
│   │   ├── CalendarView.tsx
│   │   └── MonthlyChart.tsx
│   └── advisors/
│       ├── AdvisorSelector.tsx
│       ├── FarmingAdvisor.tsx
│       ├── MoodAdvisor.tsx
│       └── FashionAdvisor.tsx
├── lib/
│   ├── api.ts
│   ├── utils.ts
│   └── types.ts
├── stores/
│   ├── vibeStore.ts
│   ├── locationStore.ts
│   └── uiStore.ts
├── styles/
│   └── globals.css
├── public/
│   ├── icons/
│   └── images/
└── package.json
```

### 5.3 Component Specifications

#### 5.3.1 VibeSelector Component
**Purpose:** Allow users to select a vibe

**Props:**
```typescript
interface VibeSelectorProps {
  vibes: Vibe[];
  selectedVibe: string | null;
  onSelect: (vibeId: string) => void;
  layout?: 'grid' | 'list' | 'dropdown';
}
```

**Features:**
- Display vibe icons and names
- Highlight selected vibe
- Show vibe description on hover
- Responsive layout

#### 5.3.2 HeatmapView Component
**Purpose:** Display interactive heatmap of vibe scores

**Props:**
```typescript
interface HeatmapViewProps {
  heatmapData: GeoJSON.FeatureCollection;
  center: [number, number];
  zoom: number;
  onLocationClick: (location: Location) => void;
}
```

**Features:**
- Render Mapbox map with heatmap layer
- Color-coded based on scores (0-100)
- Zoom and pan controls
- Location marker on click
- Tooltip with score on hover

#### 5.3.3 CalendarView Component
**Purpose:** Display monthly vibe scores as calendar

**Props:**
```typescript
interface CalendarViewProps {
  monthlyScores: MonthScore[];
  onMonthClick: (month: number) => void;
  highlightBest?: boolean;
}
```

**Features:**
- Display 12 months in grid/list
- Color-code by score
- Highlight best months
- Show score numbers
- Interactive month selection

---

### 5.4 State Management

#### 5.4.1 Vibe Store
```typescript
interface VibeStore {
  vibes: Vibe[];
  selectedVibe: string | null;
  setSelectedVibe: (vibeId: string) => void;
  fetchVibes: () => Promise<void>;
}
```

#### 5.4.2 Location Store
```typescript
interface LocationStore {
  currentLocation: Location | null;
  searchResults: Location[];
  setLocation: (location: Location) => void;
  searchLocations: (query: string) => Promise<void>;
}
```

#### 5.4.3 UI Store
```typescript
interface UIStore {
  isLoading: boolean;
  error: string | null;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}
```

---

### 5.5 Responsive Design Requirements

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Mobile Optimizations:**
- Simplified navigation (hamburger menu)
- Single-column layouts
- Touch-optimized map controls
- Collapsible filters
- Bottom sheet for results

---

## 6. Backend Specifications

### 6.1 Technology Stack
- **Framework:** FastAPI 0.104+
- **Language:** Python 3.10+
- **Geospatial:** rasterio, geopandas, shapely
- **Data Processing:** numpy, pandas
- **Caching:** Redis
- **Testing:** pytest
- **Documentation:** OpenAPI (auto-generated)

### 6.2 Project Structure
```
server/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── where.py
│   │   ├── when.py
│   │   ├── advisor.py
│   │   └── vibes.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── vibe.py
│   │   ├── location.py
│   │   └── response.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── vibe_engine.py
│   │   ├── geotiff_reader.py
│   │   ├── scoring.py
│   │   └── cache.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── data/
│       ├── vibe_dictionary.json
│       └── geotiffs/
├── tests/
│   ├── test_api.py
│   ├── test_services.py
│   └── test_scoring.py
├── requirements.txt
└── README.md
```

### 6.3 Core Services

#### 6.3.1 Vibe Engine Service
```python
class VibeEngine:
    def __init__(self, vibe_dict_path: str, data_path: str):
        self.vibes = self.load_vibes(vibe_dict_path)
        self.data_path = data_path
        
    def calculate_score(
        self, 
        vibe_id: str, 
        location: Tuple[float, float], 
        month: int
    ) -> float:
        """Calculate vibe score for a location and month"""
        pass
        
    def generate_heatmap(
        self, 
        vibe_id: str, 
        month: int, 
        bounds: Optional[Bounds] = None
    ) -> GeoJSON:
        """Generate heatmap data for a vibe and month"""
        pass
        
    def get_monthly_scores(
        self, 
        vibe_id: str, 
        location: Tuple[float, float]
    ) -> List[float]:
        """Get scores for all 12 months"""
        pass
```

#### 6.3.2 GeoTIFF Reader Service
```python
class GeoTIFFReader:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.cache = {}
        
    def read_value(
        self, 
        file_path: str, 
        lon: float, 
        lat: float
    ) -> float:
        """Read value at specific coordinates"""
        pass
        
    def read_region(
        self, 
        file_path: str, 
        bounds: Bounds
    ) -> np.ndarray:
        """Read values for a region"""
        pass
        
    def get_file_path(
        self, 
        vibe_id: str, 
        parameter_id: str, 
        month: int
    ) -> str:
        """Get file path for specific data"""
        pass
```

#### 6.3.3 Scoring Service
```python
class ScoringService:
    @staticmethod
    def score_low_is_better(
        value: float, 
        min_val: float, 
        max_val: float
    ) -> float:
        """Score where lower is better"""
        pass
        
    @staticmethod
    def score_high_is_better(
        value: float, 
        min_val: float, 
        max_val: float
    ) -> float:
        """Score where higher is better"""
        pass
        
    @staticmethod
    def score_optimal_range(
        value: float, 
        optimal_min: float, 
        optimal_max: float
    ) -> float:
        """Score for optimal range"""
        pass
        
    @staticmethod
    def calculate_weighted_score(
        scores: Dict[str, float], 
        weights: Dict[str, float]
    ) -> float:
        """Calculate weighted final score"""
        pass
```

---

### 6.4 Pydantic Models

#### 6.4.1 Request Models
```python
class WhereRequest(BaseModel):
    vibe: str
    month: int = Field(ge=1, le=12)
    region: Optional[Bounds] = None
    resolution: Optional[str] = "medium"

class WhenRequest(BaseModel):
    vibe: str
    location: Location
    years: Optional[List[int]] = None

class AdvisorRequest(BaseModel):
    advisorType: str
    location: Location
    parameters: Dict[str, Any]
```

#### 6.4.2 Response Models
```python
class WhereResponse(BaseModel):
    success: bool
    data: WhereData
    metadata: ResponseMetadata

class WhenResponse(BaseModel):
    success: bool
    data: WhenData
    metadata: ResponseMetadata

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
    metadata: ResponseMetadata
```

---

### 6.5 Caching Strategy

**Cache Layers:**
1. **Memory Cache:** Recent queries (LRU, max 1000 items)
2. **Redis Cache:** Computed scores (TTL: 24 hours)
3. **File System Cache:** Processed GeoJSON (persistent)

**Cache Keys:**
```
where:{vibe_id}:{month}:{region_hash}
when:{vibe_id}:{location_hash}
advisor:{advisor_type}:{location_hash}:{params_hash}
```

---

## 7. Integration Specifications

### 7.1 Frontend-Backend Integration

**API Client Configuration:**
```typescript
// lib/api.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use((config) => {
  // Add auth token if available
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // Handle errors globally
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

### 7.2 Mapbox Integration

**Configuration:**
```typescript
const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;

const mapConfig = {
  style: 'mapbox://styles/mapbox/light-v11',
  center: [77.5946, 12.9716], // Bangalore
  zoom: 8,
  maxBounds: [
    [68, 8],   // Southwest
    [88, 35]   // Northeast
  ],
};
```

**Heatmap Layer:**
```typescript
const heatmapLayer: LayerProps = {
  id: 'vibe-heatmap',
  type: 'heatmap',
  source: 'vibe-data',
  paint: {
    'heatmap-weight': [
      'interpolate',
      ['linear'],
      ['get', 'score'],
      0, 0,
      100, 1
    ],
    'heatmap-intensity': 1,
    'heatmap-color': [
      'interpolate',
      ['linear'],
      ['heatmap-density'],
      0, 'rgba(33,102,172,0)',
      0.2, 'rgb(103,169,207)',
      0.4, 'rgb(209,229,240)',
      0.6, 'rgb(253,219,199)',
      0.8, 'rgb(239,138,98)',
      1, 'rgb(178,24,43)'
    ],
  },
};
```

---

### 7.3 Data Pipeline Integration

**Data Flow:**
```
NASA POWER API 
    ↓
cron_job.py (fetch & process)
    ↓
GeoTIFF files (local storage)
    ↓
AWS S3 (cloud storage)
    ↓
FastAPI Backend (on-demand query)
    ↓
Next.js Frontend (display)
```

**cron_job.py Specification:**
```python
"""
Data fetching and processing script
Runs: Weekly (or on-demand for hackathon)
"""

import requests
import rasterio
import numpy as np
from datetime import datetime

class DataPipeline:
    def __init__(self, config):
        self.nasa_base_url = "https://power.larc.nasa.gov/api/"
        self.output_dir = "data/geotiffs/"
        self.vibes = self.load_vibes()
        
    def fetch_all_data(self):
        """Fetch data for all vibes and months"""
        for vibe in self.vibes:
            for month in range(1, 13):
                self.fetch_vibe_month(vibe, month)
                
    def fetch_vibe_month(self, vibe, month):
        """Fetch and process data for a vibe and month"""
        for param in vibe.parameters:
            # Fetch from NASA API
            data = self.fetch_nasa_data(param, month)
            
            # Process to GeoTIFF
            geotiff = self.process_to_geotiff(data)
            
            # Save locally
            self.save_geotiff(geotiff, vibe, param, month)
            
    def upload_to_s3(self):
        """Upload processed files to S3"""
        pass
```

---

## 8. Performance Requirements

### 8.1 Response Time Targets

| Endpoint | Target | Maximum | Notes |
|----------|--------|---------|-------|
| /api/where | 1.5s | 3s | Includes data query and processing |
| /api/when | 1s | 2s | Simpler query, less data |
| /api/advisor | 1s | 2.5s | Depends on advisor type |
| /api/vibes | 100ms | 500ms | Static data, should be cached |

### 8.2 Optimization Strategies

**Backend:**
- Pre-compute common queries
- Implement Redis caching
- Use connection pooling
- Optimize GeoTIFF reading (windowed reads)
- Implement pagination for large results

**Frontend:**
- Code splitting (Next.js automatic)
- Image optimization
- Lazy loading for map layers
- Debounce search inputs
- Use React.memo for expensive components

### 8.3 Scalability Requirements

**Concurrent Users:**
- Target: 1000 concurrent users
- Peak: 5000 concurrent users (during demo)

**Data Volume:**
- Total GeoTIFF storage: ~10-50 GB
- API response sizes: < 2 MB per request
- Cache storage: ~5 GB Redis

---

## 9. Security Requirements

### 9.1 API Security

**CORS Configuration:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://weathervibes.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

**Rate Limiting:**
- 100 requests per minute per IP
- 1000 requests per hour per user
- Implement using SlowAPI or Redis

**Input Validation:**
- Validate all user inputs with Pydantic
- Sanitize location search queries
- Limit coordinate ranges to valid bounds
- Validate month ranges (1-12)

### 9.2 Data Security

**Storage:**
- Use environment variables for sensitive config
- Implement access control for S3 buckets
- Encrypt data in transit (HTTPS)
- No sensitive user data stored

**API Keys:**
- Store in .env files (not in git)
- Rotate keys regularly
- Use different keys for dev/prod

---

## 10. Testing Requirements

### 10.1 Backend Testing

**Unit Tests:**
```python
# tests/test_scoring.py
def test_score_low_is_better():
    score = score_low_is_better(20, 0, 100)
    assert score == 80
    
def test_calculate_weighted_score():
    scores = {"CLOUD_AMT": 80, "RH2M": 60}
    weights = {"CLOUD_AMT": 0.6, "RH2M": 0.4}
    final = calculate_weighted_score(scores, weights)
    assert final == 72
```

**Integration Tests:**
```python
# tests/test_api.py
def test_where_endpoint():
    response = client.get("/api/where?vibe=stargazing&month=7")
    assert response.status_code == 200
    assert "heatmap" in response.json()["data"]
```

**Coverage Target:** 80%+

### 10.2 Frontend Testing

**Component Tests:**
```typescript
// __tests__/VibeSelector.test.tsx
describe('VibeSelector', () => {
  it('renders all vibes', () => {
    render(<VibeSelector vibes={mockVibes} />);
    expect(screen.getByText('Perfect Stargazing')).toBeInTheDocument();
  });
  
  it('calls onSelect when vibe clicked', () => {
    const onSelect = jest.fn();
    render(<VibeSelector vibes={mockVibes} onSelect={onSelect} />);
    fireEvent.click(screen.getByText('Perfect Stargazing'));
    expect(onSelect).toHaveBeenCalledWith('stargazing');
  });
});
```

**E2E Tests:**
- Use Playwright or Cypress
- Test complete user flows
- Test on multiple browsers

---

## 11. Documentation Requirements

### 11.1 Required Documentation

**Code Documentation:**
- Inline comments for complex logic
- Docstrings for all functions (Python)
- JSDoc for TypeScript functions
- README for each major component

**API Documentation:**
- Auto-generated OpenAPI/Swagger docs
- Example requests and responses
- Error code descriptions
- Rate limiting info

**User Documentation:**
- User guide (how to use the app)
- FAQ section
- Vibe descriptions
- Data sources and attribution

---

**End of Technical Specification**

*This document defines what needs to be built and how it should function. Refer to DESIGN.md for architectural details and PLAN.md for development schedule.*

