# Backend Integration Guide

This guide explains how to integrate the Next.js frontend with the FastAPI backend.

## API Architecture

### Base URL Configuration

The API base URL is configured via environment variable:

```bash
# .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

For production:
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.weathervibes.com
```

### Axios Instance

All API calls use a configured Axios instance (`src/services/api.ts`):

```typescript
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

**Features**:
- Automatic base URL prefixing
- 30-second timeout
- JSON content type by default
- Request/response interceptors for logging

---

## Feature 1: Where (Vivek)

### Overview
Find the best locations for a vibe in a specific month.

### Frontend Implementation

**Component**: `src/components/features/where/WherePanel.tsx`

**Service**: `src/services/whereService.ts`

```typescript
export const whereService = {
  getHeatmap: async (request: WhereRequest): Promise<WhereResponse> => {
    const response = await api.post<WhereResponse>('/api/where', request);
    return response.data;
  },
};
```

### Backend Endpoint Specification

**Endpoint**: `POST /api/where`

**Request Body**:
```typescript
{
  vibeId: string;        // e.g., "stargazing"
  month: number;         // 1-12
  year?: number;         // Optional, defaults to current year
  bounds: {
    north: number;       // Max latitude
    south: number;       // Min latitude
    east: number;        // Max longitude
    west: number;        // Min longitude
  };
}
```

**Example Request**:
```json
{
  "vibeId": "stargazing",
  "month": 7,
  "year": 2024,
  "bounds": {
    "north": 13.5,
    "south": 12.5,
    "east": 78.0,
    "west": 77.0
  }
}
```

**Response Body**:
```typescript
{
  heatmapData: {
    type: 'FeatureCollection';
    features: Array<{
      type: 'Feature';
      geometry: {
        type: 'Point';
        coordinates: [number, number];  // [lng, lat]
      };
      properties: {
        score: number;  // 0-100
      };
    }>;
  };
  topLocations: Array<{
    name: string;           // e.g., "Bangalore"
    coordinates: [number, number];  // [lng, lat]
    score: number;          // 0-100
  }>;
}
```

**Example Response**:
```json
{
  "heatmapData": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [77.5946, 12.9716]
        },
        "properties": {
          "score": 85.5
        }
      }
    ]
  },
  "topLocations": [
    {
      "name": "Bangalore",
      "coordinates": [77.5946, 12.9716],
      "score": 85.5
    },
    {
      "name": "Mysore",
      "coordinates": [76.6394, 12.2958],
      "score": 82.3
    }
  ]
}
```

### Frontend Integration Steps

1. **User Flow**:
   - User selects vibe from dropdown
   - User selects month from dropdown
   - User adjusts map to desired region
   - User clicks "Find Best Locations"

2. **Data Collection**:
```typescript
const handleFindLocations = async () => {
  const { selectedVibe } = useVibeStore.getState();
  const { selectedMonth } = useTimeStore.getState();
  const { bounds } = useLocationStore.getState();

  const request: WhereRequest = {
    vibeId: selectedVibe.id,
    month: selectedMonth,
    bounds: {
      north: bounds[1][1],
      south: bounds[0][1],
      east: bounds[1][0],
      west: bounds[0][0],
    },
  };

  const response = await whereService.getHeatmap(request);
  // Handle response
};
```

3. **Response Handling**:
   - Add heatmap layer to Mapbox map
   - Display top locations list
   - Show loading state during request

### TODO for Vivek:
- [ ] Implement `/api/where` endpoint
- [ ] Calculate scores for grid points within bounds
- [ ] Return GeoJSON FeatureCollection
- [ ] Include top 5 locations with names
- [ ] Handle errors (invalid vibe, out of bounds, etc.)

### TODO for Bhawesh:
- [ ] Add Mapbox heatmap layer visualization
- [ ] Display top locations list
- [ ] Add loading spinner
- [ ] Handle errors gracefully

---

## Feature 2: When

### Overview
Find the best months for a vibe at a specific location.

### Frontend Implementation

**Component**: `src/components/features/when/WhenPanel.tsx`

**Service**: `src/services/whenService.ts`

```typescript
export const whenService = {
  getMonthlyScores: async (request: WhenRequest): Promise<WhenResponse> => {
    const response = await api.post<WhenResponse>('/api/when', request);
    return response.data;
  },
};
```

### Backend Endpoint Specification

**Endpoint**: `POST /api/when`

**Request Body**:
```typescript
{
  vibeId: string;              // e.g., "beach_day"
  location: [number, number];  // [lng, lat]
  year?: number;               // Optional, defaults to current year
}
```

**Example Request**:
```json
{
  "vibeId": "beach_day",
  "location": [77.5946, 12.9716],
  "year": 2024
}
```

**Response Body**:
```typescript
{
  monthlyScores: Array<{
    month: number;              // 1-12
    score: number;              // 0-100
    details?: {
      temperature?: number;
      rainfall?: number;
      humidity?: number;
      // Other relevant weather params
    };
  }>;
}
```

**Example Response**:
```json
{
  "monthlyScores": [
    {
      "month": 1,
      "score": 45.2,
      "details": {
        "temperature": 22.5,
        "rainfall": 5.2,
        "humidity": 68
      }
    },
    {
      "month": 2,
      "score": 52.8,
      "details": {
        "temperature": 24.1,
        "rainfall": 3.8,
        "humidity": 65
      }
    },
    // ... months 3-12
  ]
}
```

### Frontend Integration Steps

1. **User Flow**:
   - User selects vibe
   - User positions map at desired location
   - User clicks "Find Best Times"

2. **Data Collection**:
```typescript
const handleFindBestTimes = async () => {
  const { selectedVibe } = useVibeStore.getState();
  const { center } = useLocationStore.getState();

  const request: WhenRequest = {
    vibeId: selectedVibe.id,
    location: center,  // [lng, lat]
    year: new Date().getFullYear(),
  };

  const response = await whenService.getMonthlyScores(request);
  // Open calendar modal with scores
};
```

3. **Response Handling**:
   - Open calendar modal
   - Display monthly scores as bar chart
   - Highlight best months
   - Show details on hover/click

### TODO (Backend):
- [ ] Implement `/api/when` endpoint
- [ ] Calculate monthly scores for location
- [ ] Include weather parameter details
- [ ] Handle invalid locations

### TODO (Frontend):
- [ ] Create CalendarModal component
- [ ] Integrate Recharts for visualization
- [ ] Add month detail view
- [ ] Show loading state

---

## Feature 3: AI Advisors (Kiran)

### Overview
Get AI-powered recommendations based on weather conditions.

### Frontend Implementation

**Component**: `src/components/features/advisors/AdvisorPanel.tsx`

**Service**: `src/services/advisorService.ts`

```typescript
export const advisorService = {
  getRecommendations: async (request: AdvisorRequest): Promise<AdvisorResponse> => {
    const response = await api.post<AdvisorResponse>('/api/advisor', request);
    return response.data;
  },
};
```

### Backend Endpoint Specification

**Endpoint**: `POST /api/advisor`

**Request Body**:
```typescript
{
  advisorId: string;           // "fashion_stylist" | "crop_advisor" | "mood_predictor"
  location: [number, number];  // [lng, lat]
  date?: string;               // ISO 8601 date, defaults to today
}
```

**Example Request**:
```json
{
  "advisorId": "fashion_stylist",
  "location": [77.5946, 12.9716],
  "date": "2024-07-15"
}
```

**Response Body**:
```typescript
{
  type: string;                // Advisor type
  recommendations: Array<{
    item: string;              // Recommendation text
    icon?: string;             // Emoji or icon identifier
    description?: string;      // Detailed explanation
  }>;
}
```

### Advisor-Specific Responses

#### Fashion Stylist
```json
{
  "type": "fashion",
  "recommendations": [
    {
      "item": "Light cotton t-shirt",
      "icon": "👕",
      "description": "Temperature expected around 28°C, breathable fabric recommended"
    },
    {
      "item": "Sunglasses",
      "icon": "🕶️",
      "description": "High UV index expected, protect your eyes"
    },
    {
      "item": "Sunscreen",
      "icon": "🧴",
      "description": "Strong sun exposure, SPF 50+ recommended"
    }
  ]
}
```

#### Crop Advisor
```json
{
  "type": "farming",
  "recommendations": [
    {
      "item": "Plant tomatoes",
      "icon": "🍅",
      "description": "Ideal temperature (22-26°C) and moderate rainfall expected"
    },
    {
      "item": "Irrigate morning crops",
      "icon": "💧",
      "description": "Low rainfall predicted for next 7 days"
    },
    {
      "item": "Avoid planting cucumbers",
      "icon": "🥒",
      "description": "High humidity may cause fungal issues"
    }
  ]
}
```

#### Mood Predictor
```json
{
  "type": "wellness",
  "recommendations": [
    {
      "item": "Morning walk",
      "icon": "🚶",
      "description": "Pleasant temperature and low humidity, great for outdoor activity"
    },
    {
      "item": "Stay hydrated",
      "icon": "💧",
      "description": "Warm weather expected, drink 8-10 glasses of water"
    },
    {
      "item": "Indoor activities afternoon",
      "icon": "🏠",
      "description": "Peak heat and UV between 12-3 PM, stay indoors"
    }
  ]
}
```

### Frontend Integration Steps

1. **User Flow**:
   - User selects AI advisor from vibe dropdown
   - User positions map at location
   - User clicks "Get Recommendations"

2. **Data Collection**:
```typescript
const handleGetAdvice = async () => {
  const { selectedVibe } = useVibeStore.getState();
  const { center } = useLocationStore.getState();

  if (selectedVibe.type !== 'advisor') {
    alert('Please select an AI advisor');
    return;
  }

  const request: AdvisorRequest = {
    advisorId: selectedVibe.id,
    location: center,
    date: new Date().toISOString().split('T')[0],
  };

  const response = await advisorService.getRecommendations(request);
  // Display recommendations
};
```

3. **Response Handling**:
   - Display recommendations as cards
   - Show icon, item, and description
   - Group by type if multiple recommendations

### TODO for Kiran:
- [ ] Implement `/api/advisor` endpoint
- [ ] Create rule engines for each advisor type
- [ ] Integrate weather data
- [ ] Generate contextual recommendations
- [ ] Add logic for fashion rules
- [ ] Add logic for crop rules
- [ ] Add logic for mood rules

### TODO for Frontend:
- [ ] Create RecommendationCard component
- [ ] Add animations for card appearance
- [ ] Handle empty recommendations
- [ ] Add loading state

---

## Error Handling

### Backend Error Format

All endpoints should return errors in this format:

```json
{
  "error": {
    "code": "VIBE_NOT_FOUND",
    "message": "Vibe 'invalid_vibe' not found",
    "details": {}
  }
}
```

### Frontend Error Handling

```typescript
try {
  const response = await whereService.getHeatmap(request);
  // Handle success
} catch (error) {
  if (axios.isAxiosError(error)) {
    const apiError = error.response?.data?.error;
    console.error('API Error:', apiError);
    // Show toast notification with error message
  } else {
    console.error('Unexpected error:', error);
    // Show generic error message
  }
}
```

### Common Error Codes

- `VIBE_NOT_FOUND` - Invalid vibe ID
- `INVALID_LOCATION` - Location out of bounds or invalid
- `INVALID_DATE` - Date format incorrect or out of range
- `NO_DATA_AVAILABLE` - No weather data for requested parameters
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `SERVER_ERROR` - Internal server error

---

## CORS Configuration

### Backend (FastAPI)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://weathervibes.com"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Integration

### Manual Testing

1. **Start Backend**:
```bash
cd server
uvicorn main:app --reload
```

2. **Start Frontend**:
```bash
cd client
npm run dev
```

3. **Test Flow**:
   - Open http://localhost:3000
   - Select a vibe
   - Click a feature button
   - Verify API call in Network tab
   - Check response data

### API Testing with curl

**Where Feature**:
```bash
curl -X POST http://localhost:8000/api/where \
  -H "Content-Type: application/json" \
  -d '{
    "vibeId": "stargazing",
    "month": 7,
    "bounds": {
      "north": 13.5,
      "south": 12.5,
      "east": 78.0,
      "west": 77.0
    }
  }'
```

**When Feature**:
```bash
curl -X POST http://localhost:8000/api/when \
  -H "Content-Type: application/json" \
  -d '{
    "vibeId": "beach_day",
    "location": [77.5946, 12.9716],
    "year": 2024
  }'
```

**Advisor Feature**:
```bash
curl -X POST http://localhost:8000/api/advisor \
  -H "Content-Type: application/json" \
  -d '{
    "advisorId": "fashion_stylist",
    "location": [77.5946, 12.9716]
  }'
```

---

## React Query Integration (Optional)

For better caching and background updates:

```typescript
import { useQuery } from '@tanstack/react-query';

function WherePanel() {
  const { selectedVibe } = useVibeStore();
  const { selectedMonth } = useTimeStore();
  const { bounds } = useLocationStore();

  const { data, isLoading, error } = useQuery({
    queryKey: ['where', selectedVibe?.id, selectedMonth, bounds],
    queryFn: () => whereService.getHeatmap({
      vibeId: selectedVibe!.id,
      month: selectedMonth!,
      bounds: {
        north: bounds![1][1],
        south: bounds![0][1],
        east: bounds![1][0],
        west: bounds![0][0],
      },
    }),
    enabled: !!selectedVibe && !!selectedMonth && !!bounds,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Render logic
}
```

**Benefits**:
- Automatic caching
- Background refetching
- Loading and error states managed
- Query invalidation

---

## Integration Checklist

### For Each Feature:

Backend:
- [ ] Implement API endpoint
- [ ] Add request validation
- [ ] Add error handling
- [ ] Test with sample data
- [ ] Document response format
- [ ] Configure CORS

Frontend:
- [ ] Update service if needed
- [ ] Add loading state
- [ ] Add error handling
- [ ] Test with real API
- [ ] Add UI for response data
- [ ] Update documentation

---

## Deployment

### Environment Variables

**Frontend (.env.local)**:
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.weathervibes.com
NEXT_PUBLIC_MAPBOX_TOKEN=your_production_token
```

**Backend**:
```bash
DATABASE_URL=postgresql://...
NASA_API_KEY=your_nasa_key
ALLOWED_ORIGINS=https://weathervibes.com
```

### API Base URL by Environment

- **Development**: `http://localhost:8000`
- **Staging**: `https://api-staging.weathervibes.com`
- **Production**: `https://api.weathervibes.com`

---

**Last Updated**: 2025-10-04
