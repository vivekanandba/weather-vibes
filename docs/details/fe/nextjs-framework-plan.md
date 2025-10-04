# Next.js Framework Plan for Weather Vibes Client

## 1. Project Initialization

### Create Next.js App
```bash
cd client
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

**Configuration choices:**
- TypeScript: Yes
- ESLint: Yes
- Tailwind CSS: Yes
- `src/` directory: Yes
- App Router: Yes
- Import alias: `@/*`

---

## 2. Dependencies

### Core Dependencies
```json
{
  "dependencies": {
    "@chakra-ui/react": "^2.8.2",
    "@chakra-ui/next-js": "^2.2.0",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "framer-motion": "^10.16.4",
    "mapbox-gl": "^3.0.1",
    "react-map-gl": "^7.1.7",
    "zustand": "^4.4.7",
    "axios": "^1.6.2",
    "recharts": "^2.10.3",
    "date-fns": "^3.0.6",
    "lodash": "^4.17.21",
    "@tanstack/react-query": "^5.14.2"
  },
  "devDependencies": {
    "@types/mapbox-gl": "^3.0.0",
    "@types/lodash": "^4.14.202"
  }
}
```

### Install Command
```bash
npm install @chakra-ui/react @chakra-ui/next-js @emotion/react @emotion/styled framer-motion mapbox-gl react-map-gl zustand axios recharts date-fns lodash @tanstack/react-query
npm install -D @types/mapbox-gl @types/lodash
```

---

## 3. Project Structure

```
client/
├── public/
│   ├── favicon.ico
│   ├── icons/                      # Vibe icons
│   └── images/                     # App images
│
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout with providers
│   │   ├── page.tsx                # Main map view page
│   │   ├── globals.css             # Global styles
│   │   └── providers.tsx           # Client-side providers wrapper
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx          # Top navigation bar
│   │   │   ├── Sidebar.tsx         # Side panel for filters
│   │   │   └── Footer.tsx          # Optional footer
│   │   │
│   │   ├── map/
│   │   │   ├── MapView.tsx         # Main Mapbox map component
│   │   │   ├── HeatmapLayer.tsx    # Heatmap overlay for "Where"
│   │   │   ├── LocationMarker.tsx  # Location pins
│   │   │   └── MapControls.tsx     # Zoom, navigation controls
│   │   │
│   │   ├── vibe/
│   │   │   ├── VibeSelector.tsx    # Dropdown/modal for vibe selection
│   │   │   ├── VibeCard.tsx        # Individual vibe display card
│   │   │   └── VibeIcon.tsx        # Icon component for vibes
│   │   │
│   │   ├── features/
│   │   │   ├── where/
│   │   │   │   ├── WherePanel.tsx      # Controls for "Where" feature
│   │   │   │   ├── LocationResults.tsx # List of top locations
│   │   │   │   └── HeatmapLegend.tsx   # Color scale legend
│   │   │   │
│   │   │   ├── when/
│   │   │   │   ├── WhenPanel.tsx       # Controls for "When" feature
│   │   │   │   ├── CalendarModal.tsx   # Monthly calendar view
│   │   │   │   ├── MonthlyChart.tsx    # Bar chart for scores
│   │   │   │   └── ScoreCard.tsx       # Score display card
│   │   │   │
│   │   │   └── advisors/
│   │   │       ├── AdvisorPanel.tsx      # Advisor selection
│   │   │       ├── AdvisorCard.tsx       # Recommendation card
│   │   │       ├── FashionAdvisor.tsx    # Fashion stylist UI
│   │   │       ├── CropAdvisor.tsx       # Farming advisor UI
│   │   │       └── MoodAdvisor.tsx       # Climate mood UI
│   │   │
│   │   └── ui/
│   │       ├── Button.tsx          # Reusable button
│   │       ├── Card.tsx            # Card container
│   │       ├── Modal.tsx           # Modal wrapper
│   │       ├── Loading.tsx         # Loading spinner
│   │       └── ErrorBoundary.tsx   # Error handling
│   │
│   ├── stores/
│   │   ├── useVibeStore.ts         # Selected vibe state
│   │   ├── useLocationStore.ts     # Location/map state
│   │   ├── useTimeStore.ts         # Time range state
│   │   └── useUIStore.ts           # UI state (modals, panels)
│   │
│   ├── services/
│   │   ├── api.ts                  # Axios instance configuration
│   │   ├── whereService.ts         # API calls for "Where" feature
│   │   ├── whenService.ts          # API calls for "When" feature
│   │   └── advisorService.ts       # API calls for "Advisors"
│   │
│   ├── types/
│   │   ├── vibe.ts                 # Vibe-related types
│   │   ├── location.ts             # Location/coordinate types
│   │   ├── api.ts                  # API request/response types
│   │   └── index.ts                # Type exports
│   │
│   ├── utils/
│   │   ├── scoring.ts              # Score calculation helpers
│   │   ├── formatting.ts           # Date/number formatting
│   │   ├── mapHelpers.ts           # Mapbox utility functions
│   │   └── constants.ts            # App constants
│   │
│   ├── config/
│   │   ├── vibes.ts                # Vibe dictionary (frontend copy)
│   │   ├── theme.ts                # Chakra UI theme customization
│   │   └── mapbox.ts               # Mapbox configuration
│   │
│   └── hooks/
│       ├── useDebounce.ts          # Debounce hook
│       ├── useGeolocation.ts       # User location hook
│       └── useMediaQuery.ts        # Responsive design hook
│
├── .env.local                      # Environment variables
├── .env.example                    # Example env file
├── next.config.js                  # Next.js configuration
├── tsconfig.json                   # TypeScript configuration
├── tailwind.config.js              # Tailwind configuration
└── package.json
```

---

## 4. Configuration Files

### 4.1 Environment Variables (`.env.local`)
```env
# Backend API
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Mapbox
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here

# App Configuration
NEXT_PUBLIC_DEFAULT_LAT=12.9716
NEXT_PUBLIC_DEFAULT_LNG=77.5946
NEXT_PUBLIC_DEFAULT_ZOOM=10
```

### 4.2 Next.js Configuration (`next.config.js`)
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    // Fix for mapbox-gl
    config.module.rules.push({
      test: /\.mjs$/,
      include: /node_modules/,
      type: 'javascript/auto',
    });
    return config;
  },
  // Ignore build errors for mapbox-gl
  transpilePackages: ['mapbox-gl'],
};

module.exports = nextConfig;
```

### 4.3 TypeScript Configuration (`tsconfig.json`)
```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@stores/*": ["./src/stores/*"],
      "@services/*": ["./src/services/*"],
      "@types/*": ["./src/types/*"],
      "@utils/*": ["./src/utils/*"],
      "@config/*": ["./src/config/*"],
      "@hooks/*": ["./src/hooks/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### 4.4 Tailwind Configuration (`tailwind.config.js`)
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#e3f2fd',
          100: '#bbdefb',
          500: '#2196f3',
          600: '#1e88e5',
          700: '#1976d2',
        },
      },
    },
  },
  plugins: [],
};
```

---

## 5. Core Implementation Files

### 5.1 Providers Setup (`src/app/providers.tsx`)
```typescript
'use client';

import { ChakraProvider } from '@chakra-ui/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import theme from '@config/theme';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider theme={theme}>
        {children}
      </ChakraProvider>
    </QueryClientProvider>
  );
}
```

### 5.2 Root Layout (`src/app/layout.tsx`)
```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from './providers';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Weather Vibes - Find Your Perfect Weather',
  description: 'Theme-based weather discovery engine powered by NASA data',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### 5.3 Chakra UI Theme (`src/config/theme.ts`)
```typescript
import { extendTheme, type ThemeConfig } from '@chakra-ui/react';

const config: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: false,
};

const theme = extendTheme({
  config,
  colors: {
    brand: {
      50: '#e3f2fd',
      100: '#bbdefb',
      200: '#90caf9',
      300: '#64b5f6',
      400: '#42a5f5',
      500: '#2196f3',
      600: '#1e88e5',
      700: '#1976d2',
      800: '#1565c0',
      900: '#0d47a1',
    },
  },
  fonts: {
    heading: 'Inter, system-ui, sans-serif',
    body: 'Inter, system-ui, sans-serif',
  },
});

export default theme;
```

---

## 6. State Management (Zustand Stores)

### 6.1 Vibe Store (`src/stores/useVibeStore.ts`)
```typescript
import { create } from 'zustand';
import { Vibe } from '@types/vibe';

interface VibeStore {
  selectedVibe: Vibe | null;
  setSelectedVibe: (vibe: Vibe | null) => void;
  activeFeature: 'where' | 'when' | 'advisor' | null;
  setActiveFeature: (feature: 'where' | 'when' | 'advisor' | null) => void;
}

export const useVibeStore = create<VibeStore>((set) => ({
  selectedVibe: null,
  setSelectedVibe: (vibe) => set({ selectedVibe: vibe }),
  activeFeature: null,
  setActiveFeature: (feature) => set({ activeFeature: feature }),
}));
```

### 6.2 Location Store (`src/stores/useLocationStore.ts`)
```typescript
import { create } from 'zustand';
import { LngLatLike } from 'mapbox-gl';

interface LocationStore {
  center: LngLatLike;
  zoom: number;
  bounds: [[number, number], [number, number]] | null;
  setCenter: (center: LngLatLike) => void;
  setZoom: (zoom: number) => void;
  setBounds: (bounds: [[number, number], [number, number]]) => void;
}

export const useLocationStore = create<LocationStore>((set) => ({
  center: [77.5946, 12.9716], // Bangalore
  zoom: 10,
  bounds: null,
  setCenter: (center) => set({ center }),
  setZoom: (zoom) => set({ zoom }),
  setBounds: (bounds) => set({ bounds }),
}));
```

### 6.3 Time Store (`src/stores/useTimeStore.ts`)
```typescript
import { create } from 'zustand';

interface TimeStore {
  selectedMonth: number | null;
  selectedYear: number;
  timeRange: { start: Date; end: Date } | null;
  setSelectedMonth: (month: number) => void;
  setSelectedYear: (year: number) => void;
  setTimeRange: (range: { start: Date; end: Date }) => void;
}

export const useTimeStore = create<TimeStore>((set) => ({
  selectedMonth: new Date().getMonth() + 1,
  selectedYear: new Date().getFullYear(),
  timeRange: null,
  setSelectedMonth: (month) => set({ selectedMonth: month }),
  setSelectedYear: (year) => set({ selectedYear: year }),
  setTimeRange: (range) => set({ timeRange: range }),
}));
```

---

## 7. TypeScript Types

### 7.1 Vibe Types (`src/types/vibe.ts`)
```typescript
export interface VibeParameter {
  id: string;
  weight: number;
  scoring: 'low_is_better' | 'high_is_better' | 'optimal_range';
  range?: [number, number];
}

export interface Vibe {
  id: string;
  name: string;
  description?: string;
  icon?: string;
  type?: 'standard' | 'advisor';
  parameters: VibeParameter[];
  logic?: string;
}

export interface VibeScore {
  vibeId: string;
  score: number;
  location?: [number, number];
  month?: number;
  details?: Record<string, any>;
}
```

### 7.2 API Types (`src/types/api.ts`)
```typescript
export interface WhereRequest {
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

export interface WhereResponse {
  heatmapData: {
    type: 'FeatureCollection';
    features: Array<{
      type: 'Feature';
      geometry: {
        type: 'Point';
        coordinates: [number, number];
      };
      properties: {
        score: number;
      };
    }>;
  };
  topLocations: Array<{
    name: string;
    coordinates: [number, number];
    score: number;
  }>;
}

export interface WhenRequest {
  vibeId: string;
  location: [number, number];
  year?: number;
}

export interface WhenResponse {
  monthlyScores: Array<{
    month: number;
    score: number;
    details?: Record<string, any>;
  }>;
}

export interface AdvisorRequest {
  advisorId: string;
  location: [number, number];
  date?: string;
}

export interface AdvisorResponse {
  type: string;
  recommendations: Array<{
    item: string;
    icon?: string;
    description?: string;
  }>;
}
```

---

## 8. API Service Layer

### 8.1 API Client (`src/services/api.ts`)
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
    // Add any auth tokens here if needed
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

### 8.2 Where Service (`src/services/whereService.ts`)
```typescript
import api from './api';
import { WhereRequest, WhereResponse } from '@types/api';

export const whereService = {
  getHeatmap: async (request: WhereRequest): Promise<WhereResponse> => {
    const response = await api.post<WhereResponse>('/api/where', request);
    return response.data;
  },
};
```

### 8.3 When Service (`src/services/whenService.ts`)
```typescript
import api from './api';
import { WhenRequest, WhenResponse } from '@types/api';

export const whenService = {
  getMonthlyScores: async (request: WhenRequest): Promise<WhenResponse> => {
    const response = await api.post<WhenResponse>('/api/when', request);
    return response.data;
  },
};
```

---

## 9. Main Page (`src/app/page.tsx`)

```typescript
'use client';

import { Box, Flex } from '@chakra-ui/react';
import Header from '@components/layout/Header';
import Sidebar from '@components/layout/Sidebar';
import MapView from '@components/map/MapView';
import WherePanel from '@components/features/where/WherePanel';
import WhenPanel from '@components/features/when/WhenPanel';
import AdvisorPanel from '@components/features/advisors/AdvisorPanel';
import { useVibeStore } from '@stores/useVibeStore';

export default function Home() {
  const { activeFeature } = useVibeStore();

  return (
    <Flex direction="column" h="100vh">
      <Header />
      <Flex flex={1} position="relative">
        <Sidebar />
        <Box flex={1} position="relative">
          <MapView />
          {activeFeature === 'where' && <WherePanel />}
          {activeFeature === 'when' && <WhenPanel />}
          {activeFeature === 'advisor' && <AdvisorPanel />}
        </Box>
      </Flex>
    </Flex>
  );
}
```

---

## 10. Vibe Dictionary Configuration

### Frontend Vibe Config (`src/config/vibes.ts`)
```typescript
import { Vibe } from '@types/vibe';

export const VIBES: Record<string, Vibe> = {
  stargazing: {
    id: 'stargazing',
    name: 'Perfect Stargazing',
    description: 'Clear skies and low humidity for optimal stargazing',
    icon: '🌟',
    type: 'standard',
    parameters: [
      { id: 'CLOUD_AMT', weight: 0.6, scoring: 'low_is_better' },
      { id: 'RH2M', weight: 0.4, scoring: 'low_is_better' },
    ],
  },
  beach_day: {
    id: 'beach_day',
    name: 'Ideal Beach Day',
    description: 'Sunny, warm, and minimal rain',
    icon: '🏖️',
    type: 'standard',
    parameters: [
      { id: 'ALLSKY_SFC_SW_DWN', weight: 0.4, scoring: 'high_is_better' },
      { id: 'T2M', weight: 0.4, scoring: 'optimal_range', range: [24, 32] },
      { id: 'PRECTOTCORR', weight: 0.2, scoring: 'low_is_better' },
    ],
  },
  cozy_rain: {
    id: 'cozy_rain',
    name: 'Cozy Rainy Day',
    description: 'Perfect for indoor activities with steady rain',
    icon: '🌧️',
    type: 'standard',
    parameters: [
      { id: 'PRECTOTCORR', weight: 0.7, scoring: 'high_is_better' },
      { id: 'T2M', weight: 0.3, scoring: 'optimal_range', range: [18, 24] },
    ],
  },
  kite_flying: {
    id: 'kite_flying',
    name: 'Ideal Kite Flying',
    description: 'Moderate winds and clear skies',
    icon: '🪁',
    type: 'standard',
    parameters: [
      { id: 'WS2M', weight: 0.5, scoring: 'optimal_range', range: [10, 25] },
      { id: 'CLOUD_AMT', weight: 0.3, scoring: 'low_is_better' },
      { id: 'PRECTOTCORR', weight: 0.2, scoring: 'low_is_better' },
    ],
  },
  // Advisors
  fashion_stylist: {
    id: 'fashion_stylist',
    name: 'AI Fashion Stylist',
    description: 'Weather-appropriate outfit recommendations',
    icon: '👔',
    type: 'advisor',
    parameters: [
      { id: 'T2M', weight: 0.4, scoring: 'high_is_better' },
      { id: 'ALLSKY_SFC_SW_DWN', weight: 0.3, scoring: 'high_is_better' },
      { id: 'PRECTOTCORR', weight: 0.2, scoring: 'low_is_better' },
      { id: 'WS2M', weight: 0.1, scoring: 'low_is_better' },
    ],
    logic: 'fashion_rules',
  },
  crop_advisor: {
    id: 'crop_advisor',
    name: 'Crop & Farming Advisor',
    description: 'Optimal planting and growing conditions',
    icon: '🌾',
    type: 'advisor',
    parameters: [
      { id: 'T2M', weight: 0.3, scoring: 'optimal_range', range: [15, 30] },
      { id: 'PRECTOTCORR', weight: 0.4, scoring: 'optimal_range', range: [50, 150] },
      { id: 'T2M_MIN', weight: 0.3, scoring: 'optimal_range', range: [10, 20] },
    ],
    logic: 'crop_rules',
  },
  mood_predictor: {
    id: 'mood_predictor',
    name: 'Climate Mood Predictor',
    description: 'Wellness suggestions based on weather',
    icon: '😊',
    type: 'advisor',
    parameters: [
      { id: 'ALLSKY_SFC_SW_DWN', weight: 0.4, scoring: 'high_is_better' },
      { id: 'T2M', weight: 0.3, scoring: 'optimal_range', range: [20, 26] },
      { id: 'RH2M', weight: 0.3, scoring: 'optimal_range', range: [40, 60] },
    ],
    logic: 'mood_rules',
  },
};

export const getVibeById = (id: string): Vibe | undefined => {
  return VIBES[id];
};

export const getStandardVibes = (): Vibe[] => {
  return Object.values(VIBES).filter((v) => v.type !== 'advisor');
};

export const getAdvisorVibes = (): Vibe[] => {
  return Object.values(VIBES).filter((v) => v.type === 'advisor');
};
```

---

## 11. Implementation Sequence

### Phase 1: Foundation (Day 1)
1. Initialize Next.js project
2. Install all dependencies
3. Set up configuration files
4. Create project structure (empty folders and files)
5. Set up providers and theme
6. Test basic app runs

### Phase 2: Core Components (Day 2)
1. Implement Zustand stores
2. Create API service layer
3. Build Header and Sidebar components
4. Implement VibeSelector component
5. Set up vibe dictionary

### Phase 3: Map Integration (Day 3)
1. Implement basic MapView component
2. Add map controls
3. Test Mapbox integration
4. Create HeatmapLayer component shell
5. Create LocationMarker component

### Phase 4: Feature Shells (Day 4)
1. Create WherePanel and related components
2. Create WhenPanel and CalendarModal
3. Create AdvisorPanel and recommendation cards
4. Wire up basic interactions

### Phase 5: Integration & Polish (Day 5)
1. Connect all components to stores
2. Wire up API calls
3. Add loading states and error handling
4. Responsive design adjustments
5. Testing and bug fixes

---

## 12. Developer Handoff Notes

### For Bhawesh (Frontend Lead):
- Main focus: UI/UX, Mapbox integration, shared components
- Start with Phase 1-3, then support other team members
- Ensure responsive design works on mobile
- Consider accessibility (keyboard navigation, ARIA labels)

### For Vivek (Backend Lead, "Where" Feature Owner):
- Frontend work needed: Heatmap visualization in `WherePanel`
- Work closely with Bhawesh on MapView integration
- Ensure GeoJSON data from backend renders correctly

### For Kiran (Data Lead, "Advisors" Feature Owner):
- Frontend work needed: Advisor recommendation cards
- Create engaging UI for fashion/crop/mood advisors
- Consider adding animations for recommendations

---

## 13. Key Design Considerations

### Performance
- Use React Query for caching API responses
- Implement virtualization for large lists
- Lazy load feature panels
- Optimize Mapbox layer rendering

### User Experience
- Loading states for all async operations
- Error boundaries for graceful error handling
- Toast notifications for user feedback
- Mobile-first responsive design

### Code Quality
- TypeScript strict mode enabled
- ESLint and Prettier for code formatting
- Consistent naming conventions
- Component documentation with JSDoc

---

## 14. Environment Setup Checklist

- [ ] Node.js 18+ installed
- [ ] Create Mapbox account and get API token
- [ ] Clone repository
- [ ] Initialize Next.js project
- [ ] Install dependencies
- [ ] Create `.env.local` file
- [ ] Configure Mapbox token
- [ ] Set backend API URL
- [ ] Test development server runs
- [ ] Verify Mapbox renders correctly

---

This framework provides a complete foundation for the Weather Vibes client application. Each team member can work independently on their assigned features while sharing the common infrastructure.
