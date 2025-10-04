# Frontend Setup Summary

## Overview

A complete Next.js 14 application framework has been set up for the Weather Vibes client. The application uses modern React patterns with TypeScript, Chakra UI for the component library, Zustand for state management, and Mapbox for map visualization.

## Tech Stack

### Core Framework
- **Next.js 15.5.4** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS

### UI & Styling
- **Chakra UI v3** (installed, but v2 recommended - see Known Issues)
- **Emotion** - CSS-in-JS for Chakra UI
- **Framer Motion** - Animation library

### State Management & Data Fetching
- **Zustand 4.4.7** - Lightweight state management
- **TanStack React Query 5.14.2** - Server state management & caching

### Map Visualization
- **Mapbox GL JS 3.0.1** - WebGL-powered maps
- **React Map GL 7.1.7** - React wrapper for Mapbox

### API & Data
- **Axios 1.6.2** - HTTP client
- **Date-fns 3.0.6** - Date utilities
- **Recharts 2.10.3** - Charts for calendar visualization

## Project Structure

```
client/
├── public/                     # Static assets
│   ├── icons/                 # Vibe icons (to be added)
│   └── images/                # App images
│
├── src/
│   ├── app/                   # Next.js App Router
│   │   ├── layout.tsx        # Root layout with providers
│   │   ├── page.tsx          # Main application page
│   │   ├── providers.tsx     # Client-side providers wrapper
│   │   └── globals.css       # Global styles
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx         # Top navigation bar
│   │   │   └── Sidebar.tsx        # Left sidebar with vibe selector
│   │   │
│   │   ├── map/
│   │   │   └── MapView.tsx        # Main Mapbox map component
│   │   │
│   │   ├── vibe/
│   │   │   └── VibeSelector.tsx   # Dropdown for vibe selection
│   │   │
│   │   ├── features/
│   │   │   ├── where/
│   │   │   │   └── WherePanel.tsx      # "Where" feature UI
│   │   │   ├── when/
│   │   │   │   └── WhenPanel.tsx       # "When" feature UI
│   │   │   └── advisors/
│   │   │       └── AdvisorPanel.tsx    # "Advisors" feature UI
│   │   │
│   │   └── ui/                # Shared UI components (to be added)
│   │
│   ├── stores/                # Zustand state management
│   │   ├── useVibeStore.ts         # Selected vibe & active feature
│   │   ├── useLocationStore.ts     # Map center, zoom, bounds
│   │   ├── useTimeStore.ts         # Selected month/year
│   │   └── useUIStore.ts           # UI state (modals, sidebar)
│   │
│   ├── services/              # API client layer
│   │   ├── api.ts                  # Axios instance
│   │   ├── whereService.ts         # "Where" API calls
│   │   ├── whenService.ts          # "When" API calls
│   │   └── advisorService.ts       # "Advisors" API calls
│   │
│   ├── types/                 # TypeScript definitions
│   │   ├── vibe.ts                 # Vibe & parameter types
│   │   ├── location.ts             # Location & coordinate types
│   │   ├── api.ts                  # API request/response types
│   │   └── index.ts                # Type exports
│   │
│   ├── config/                # Configuration
│   │   ├── vibes.ts                # Vibe dictionary
│   │   ├── mapbox.ts               # Mapbox settings
│   │   └── theme.ts                # Chakra UI theme
│   │
│   ├── utils/                 # Utility functions (to be added)
│   └── hooks/                 # Custom React hooks (to be added)
│
├── .env.local                 # Environment variables (not in git)
├── .env.example               # Example env file
├── next.config.ts             # Next.js configuration
├── tsconfig.json              # TypeScript configuration
├── tailwind.config.js         # Tailwind configuration
├── package.json               # Dependencies
└── README.md                  # Setup instructions
```

## Configuration Files

### Environment Variables (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
NEXT_PUBLIC_DEFAULT_LAT=12.9716
NEXT_PUBLIC_DEFAULT_LNG=77.5946
NEXT_PUBLIC_DEFAULT_ZOOM=10
```

### TypeScript Configuration
- Strict mode enabled
- Path aliases configured:
  - `@/*` → `./src/*`
  - `@components/*` → `./src/components/*`
  - `@stores/*` → `./src/stores/*`
  - `@services/*` → `./src/services/*`
  - `@types/*` → `./src/types/*`
  - `@utils/*` → `./src/utils/*`
  - `@config/*` → `./src/config/*`
  - `@hooks/*` → `./src/hooks/*`

### Next.js Configuration
- Webpack configured for Mapbox GL JS
- Transpiles `mapbox-gl` package

## State Management Architecture

### 1. Vibe Store (`useVibeStore`)
Manages the currently selected vibe and active feature.

```typescript
interface VibeStore {
  selectedVibe: Vibe | null;
  setSelectedVibe: (vibe: Vibe | null) => void;
  activeFeature: 'where' | 'when' | 'advisor' | null;
  setActiveFeature: (feature: 'where' | 'when' | 'advisor' | null) => void;
}
```

### 2. Location Store (`useLocationStore`)
Tracks map state (center, zoom, bounds).

```typescript
interface LocationStore {
  center: [number, number];  // [lng, lat]
  zoom: number;
  bounds: [[number, number], [number, number]] | null;
  setCenter: (center: [number, number]) => void;
  setZoom: (zoom: number) => void;
  setBounds: (bounds: [[number, number], [number, number]]) => void;
}
```

### 3. Time Store (`useTimeStore`)
Manages time-related selections.

```typescript
interface TimeStore {
  selectedMonth: number | null;
  selectedYear: number;
  timeRange: { start: Date; end: Date } | null;
  setSelectedMonth: (month: number) => void;
  setSelectedYear: (year: number) => void;
  setTimeRange: (range: { start: Date; end: Date }) => void;
}
```

### 4. UI Store (`useUIStore`)
Controls UI state like modal visibility.

```typescript
interface UIStore {
  isSidebarOpen: boolean;
  isCalendarModalOpen: boolean;
  isVibeModalOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
  setCalendarModalOpen: (isOpen: boolean) => void;
  setVibeModalOpen: (isOpen: boolean) => void;
}
```

## API Integration

### Service Layer Architecture
All API calls go through service modules that use a configured Axios instance:

**Base API Client** (`api.ts`):
- Base URL from environment
- 30-second timeout
- Request/response interceptors for logging

**Feature Services**:
1. **whereService** - Get heatmap data for locations
2. **whenService** - Get monthly scores for time analysis
3. **advisorService** - Get AI recommendations

### API Request/Response Types

**Where Feature:**
```typescript
interface WhereRequest {
  vibeId: string;
  month: number;
  year?: number;
  bounds: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
}

interface WhereResponse {
  heatmapData: GeoJSON.FeatureCollection;
  topLocations: Array<{
    name: string;
    coordinates: [number, number];
    score: number;
  }>;
}
```

**When Feature:**
```typescript
interface WhenRequest {
  vibeId: string;
  location: [number, number];
  year?: number;
}

interface WhenResponse {
  monthlyScores: Array<{
    month: number;
    score: number;
    details?: Record<string, unknown>;
  }>;
}
```

**Advisors Feature:**
```typescript
interface AdvisorRequest {
  advisorId: string;
  location: [number, number];
  date?: string;
}

interface AdvisorResponse {
  type: string;
  recommendations: Array<{
    item: string;
    icon?: string;
    description?: string;
  }>;
}
```

## Vibe Dictionary

### Standard Vibes (6)
1. **Perfect Stargazing** 🌟
   - Clear skies, low humidity
   - Parameters: CLOUD_AMT (60%), RH2M (40%)

2. **Ideal Beach Day** 🏖️
   - Sunny, warm, minimal rain
   - Parameters: ALLSKY_SFC_SW_DWN (40%), T2M optimal 24-32°C (40%), PRECTOTCORR (20%)

3. **Cozy Rainy Day** 🌧️
   - Perfect for indoor activities
   - Parameters: PRECTOTCORR (70%), T2M optimal 18-24°C (30%)

4. **Ideal Kite Flying** 🪁
   - Moderate winds, clear skies
   - Parameters: WS2M optimal 10-25 km/h (50%), CLOUD_AMT (30%), PRECTOTCORR (20%)

5. **Perfect Hiking Weather** 🥾
   - Cool, dry, comfortable
   - Parameters: T2M optimal 15-25°C (40%), PRECTOTCORR (30%), WS2M (20%), RH2M (10%)

6. **Golden Hour Photography** 📸
   - Optimal lighting conditions
   - Parameters: ALLSKY_SFC_SW_DWN (50%), CLOUD_AMT optimal 20-50% (30%), RH2M (20%)

### AI Advisors (3)
1. **AI Fashion Stylist** 👔
   - Weather-appropriate outfit recommendations
   - Logic: fashion_rules

2. **Crop & Farming Advisor** 🌾
   - Optimal planting/growing conditions
   - Logic: crop_rules

3. **Climate Mood Predictor** 😊
   - Wellness suggestions based on weather
   - Logic: mood_rules

## Component Architecture

### Main Layout Structure
```
<RootLayout>
  <Providers>
    <Header />
    <Flex>
      <Sidebar />
      <MapView />
      {activeFeature === 'where' && <WherePanel />}
      {activeFeature === 'when' && <WhenPanel />}
      {activeFeature === 'advisor' && <AdvisorPanel />}
    </Flex>
  </Providers>
</RootLayout>
```

### Key Components

**Header**:
- Hamburger menu to toggle sidebar
- App title/logo
- (Color mode toggle removed temporarily)

**Sidebar**:
- Vibe selector dropdown
- Feature buttons (Where, When, Advisors)
- NASA POWER attribution

**MapView**:
- Full-screen Mapbox map
- Navigation controls
- Geolocation control
- Error handling for missing token

**VibeSelector**:
- Dropdown menu with sections
- Standard vibes section
- AI advisors section
- Shows vibe icon and description

**Feature Panels**:
- Overlay panels on map
- Context-specific controls
- API integration points
- Temporary alert() for notifications

## Implementation Status

### ✅ Complete
- Project structure and folder organization
- All type definitions
- All Zustand stores
- API service layer
- Vibe dictionary configuration
- Core layout components
- Map integration (structure)
- Feature panels (structure)
- React Query setup
- Providers configuration

### ⚠️ Needs Attention
- **Chakra UI v3 compatibility** (main blocker)
- Toast notification system (using alerts temporarily)
- Error boundaries
- Loading states
- Mapbox token required to run

### 🚧 To Be Implemented
- Heatmap layer for "Where" feature
- Calendar modal for "When" feature
- Recommendation cards for "Advisors"
- Mobile responsive design
- Error handling UI
- Loading spinners
- Unit tests

## Known Issues

### 1. Chakra UI Version Mismatch
**Problem**: Chakra UI v3 was installed, but components were written for v2 API.

**Impact**: Build fails due to breaking changes in v3:
- Component imports changed (Menu → MenuRoot/MenuTrigger/MenuContent)
- Props renamed (spacing → gap, isLoading → loading, isDisabled → disabled)
- Select component restructured
- Theme API completely different

**Solution**:
```bash
npm uninstall @chakra-ui/react @chakra-ui/next-js
npm install @chakra-ui/react@^2.8.2
```

### 2. TypeScript Path Resolution
**Problem**: `@types/` alias conflicts with TypeScript's built-in type resolution.

**Solution**: Use `@/types/` instead or relative imports for type files.

### 3. Temporary Implementations
- Toast notifications use `alert()` - replace with proper toast system
- No loading spinners yet
- Error handling is basic

## Development Workflow

### Getting Started
```bash
cd client
npm install
cp .env.example .env.local
# Add Mapbox token to .env.local
npm run dev
```

### Available Scripts
- `npm run dev` - Start development server (port 3000)
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

### Adding a New Vibe
1. Add vibe definition to `src/config/vibes.ts`
2. Include id, name, description, icon, type, and parameters
3. Define scoring logic (low_is_better, high_is_better, optimal_range)

### Integrating a New API Endpoint
1. Add request/response types to `src/types/api.ts`
2. Create service function in `src/services/`
3. Call service from component using React Query or directly

## Best Practices

### State Management
- Use Zustand for global UI state
- Use React Query for server state
- Keep component state local when possible

### API Calls
- Always use service layer, never call API directly from components
- Use React Query hooks for caching and background updates
- Handle loading and error states

### TypeScript
- Always define types for props, state, and API responses
- Use strict mode
- Prefer type over interface for unions

### Component Structure
- Keep components focused and single-responsibility
- Extract reusable logic into custom hooks
- Use composition over inheritance

## Next Steps

### Immediate (to get running)
1. Fix Chakra UI version → Downgrade to v2
2. Get Mapbox token
3. Test development server
4. Verify all features render

### Short-term (MVP)
1. Implement proper toast notifications
2. Add loading states
3. Test API integration with backend
4. Mobile responsive design

### Medium-term (Full features)
1. Heatmap visualization for "Where"
2. Calendar modal with charts for "When"
3. Recommendation cards for "Advisors"
4. Animations and transitions
5. Error boundaries
6. Unit tests

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Chakra UI v2 Docs](https://v2.chakra-ui.com/)
- [Mapbox GL JS API](https://docs.mapbox.com/mapbox-gl-js/api/)
- [Zustand Documentation](https://docs.pmnd.rs/zustand)
- [React Query Docs](https://tanstack.com/query/latest)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

**Setup Date**: 2025-10-04
**Status**: Framework complete, awaiting Chakra UI fix
