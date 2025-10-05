# Component Guide

This document provides detailed information about each component in the Weather Vibes frontend application.

## Component Hierarchy

```
App (page.tsx)
├── Header
├── Sidebar
│   └── VibeSelector
├── MapView
└── Feature Panels (conditional)
    ├── WherePanel
    ├── WhenPanel
    └── AdvisorPanel
```

## Layout Components

### Header (`components/layout/Header.tsx`)

**Purpose**: Top navigation bar with app branding and controls.

**Features**:
- Hamburger menu to toggle sidebar visibility
- App title with emoji icon
- Minimal, clean design

**State Used**:
- `useUIStore`: `isSidebarOpen`, `setSidebarOpen`

**Props**: None

**Example**:
```tsx
<Header />
```

**Future Enhancements**:
- Add color mode toggle
- User profile menu
- Notifications

---

### Sidebar (`components/layout/Sidebar.tsx`)

**Purpose**: Left sidebar containing vibe selection and feature navigation.

**Features**:
- Vibe selector dropdown
- Three feature buttons (Where, When, Advisors)
- NASA POWER attribution
- Collapsible via header toggle

**State Used**:
- `useUIStore`: `isSidebarOpen`
- `useVibeStore`: `activeFeature`, `setActiveFeature`

**Props**: None

**Styling**:
- Width: 320px
- White background
- Right border
- Scrollable content

**Feature Buttons**:
- Where 📍 - Find best locations
- When 📅 - Find best times
- Advisors 🤖 - Get AI recommendations

**Example**:
```tsx
<Sidebar />
```

---

## Vibe Components

### VibeSelector (`components/vibe/VibeSelector.tsx`)

**Purpose**: Dropdown menu for selecting a vibe or AI advisor.

**Features**:
- Displays all available vibes
- Separated into two sections:
  - Standard Vibes
  - AI Advisors
- Shows vibe icon, name, and description
- Highlights selected vibe

**State Used**:
- `useVibeStore`: `selectedVibe`, `setSelectedVibe`

**Props**: None

**Data Source**: `getStandardVibes()` and `getAdvisorVibes()` from `config/vibes.ts`

**Example**:
```tsx
<VibeSelector />
```

**Menu Structure**:
```
┌─────────────────────────┐
│ Select a vibe...      ▼ │
└─────────────────────────┘
  ┌───────────────────────────┐
  │ STANDARD VIBES            │
  │ 🌟 Perfect Stargazing     │
  │ 🏖️ Ideal Beach Day        │
  │ ...                       │
  │ ───────────────────────── │
  │ AI ADVISORS               │
  │ 👔 AI Fashion Stylist     │
  │ ...                       │
  └───────────────────────────┘
```

---

## Map Components

### MapView (`components/map/MapView.tsx`)

**Purpose**: Full-screen interactive map using Mapbox GL JS.

**Features**:
- Mapbox map with street view
- Navigation controls (zoom, rotate)
- Geolocation control (find user location)
- Error handling for missing token
- Loading spinner during initialization
- Tracks map center, zoom, and bounds

**State Used**:
- `useLocationStore`: `center`, `zoom`, `setCenter`, `setZoom`, `setBounds`

**Props**: None

**Configuration**: Uses `MAPBOX_CONFIG` from `config/mapbox.ts`

**Map Controls**:
- **Navigation Control** (top-right): Zoom in/out, rotate, pitch
- **Geolocation Control** (top-right): Center on user location

**Error States**:
- Missing/invalid Mapbox token: Shows error message with link to get token
- Map load failure: Loading spinner remains visible

**Example**:
```tsx
<MapView />
```

**Event Handlers**:
- `onLoad`: Hides loading spinner
- `onMove`: Updates center, zoom, and bounds in store

---

## Feature Panel Components

All feature panels share common characteristics:
- Positioned absolute (top-right on map)
- White background with shadow
- 300px width
- z-index: 10

### WherePanel (`components/features/where/WherePanel.tsx`)

**Purpose**: Find the best locations for a selected vibe in a given month.

**Features**:
- Month selector dropdown
- "Find Best Locations" button
- Disabled when no vibe selected
- Shows loading state during API call

**State Used**:
- `useVibeStore`: `selectedVibe`
- `useTimeStore`: `selectedMonth`, `setSelectedMonth`
- `useLocationStore`: `bounds`

**API Integration**:
- Service: `whereService.getHeatmap()`
- Request: vibeId, month, year, bounds
- Response: heatmapData (GeoJSON), topLocations

**User Flow**:
1. User selects a vibe
2. User selects a month
3. User clicks "Find Best Locations"
4. API call fetches heatmap data
5. Heatmap renders on map (TODO)
6. Top locations list displayed (TODO)

**Example**:
```tsx
{activeFeature === 'where' && <WherePanel />}
```

---

### WhenPanel (`components/features/when/WhenPanel.tsx`)

**Purpose**: Find the best times (months) for a selected vibe at current map location.

**Features**:
- Shows current map location
- "Find Best Times" button
- Disabled when no vibe selected
- Opens calendar modal on success (TODO)

**State Used**:
- `useVibeStore`: `selectedVibe`
- `useLocationStore`: `center`
- `useUIStore`: `setCalendarModalOpen`

**API Integration**:
- Service: `whenService.getMonthlyScores()`
- Request: vibeId, location, year
- Response: monthlyScores (array of month + score)

**User Flow**:
1. User selects a vibe
2. User clicks "Find Best Times"
3. API call fetches monthly scores
4. Calendar modal opens showing scores (TODO)

**Example**:
```tsx
{activeFeature === 'when' && <WhenPanel />}
```

---

### AdvisorPanel (`components/features/advisors/AdvisorPanel.tsx`)

**Purpose**: Get AI-powered recommendations based on weather and selected advisor.

**Features**:
- Shows current map location
- Shows selected advisor info (if advisor type)
- "Get Recommendations" button
- Disabled when no advisor selected
- Displays recommendations after API call (TODO)

**State Used**:
- `useVibeStore`: `selectedVibe`
- `useLocationStore`: `center`

**API Integration**:
- Service: `advisorService.getRecommendations()`
- Request: advisorId, location, date
- Response: type, recommendations (array)

**User Flow**:
1. User selects an AI advisor from vibe selector
2. User positions map at desired location
3. User clicks "Get Recommendations"
4. API call fetches recommendations
5. Recommendation cards display (TODO)

**Advisor Types**:
- **Fashion Stylist**: Outfit recommendations
- **Crop Advisor**: Planting suggestions
- **Mood Predictor**: Wellness tips

**Example**:
```tsx
{activeFeature === 'advisor' && <AdvisorPanel />}
```

---

## Component Patterns

### Using Zustand Stores

```tsx
import { useVibeStore } from '@stores/useVibeStore';

function MyComponent() {
  const { selectedVibe, setSelectedVibe } = useVibeStore();

  return (
    <div>
      Current vibe: {selectedVibe?.name || 'None'}
    </div>
  );
}
```

### Using React Query for API Calls

```tsx
import { useQuery } from '@tanstack/react-query';
import { whereService } from '@services/whereService';

function MyComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['where', vibeId, month],
    queryFn: () => whereService.getHeatmap({ vibeId, month, year, bounds }),
    enabled: !!vibeId && !!bounds, // Only run when ready
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error />;
  return <div>{/* Render data */}</div>;
}
```

### Conditional Rendering Based on Active Feature

```tsx
const { activeFeature } = useVibeStore();

return (
  <Box>
    <MapView />
    {activeFeature === 'where' && <WherePanel />}
    {activeFeature === 'when' && <WhenPanel />}
    {activeFeature === 'advisor' && <AdvisorPanel />}
  </Box>
);
```

---

## Component Props Conventions

### Common Props (Future)

When creating new components, follow these patterns:

**Layout Props**:
```typescript
interface LayoutProps {
  children?: React.ReactNode;
  className?: string;
}
```

**Data Display Props**:
```typescript
interface DataDisplayProps<T> {
  data: T;
  loading?: boolean;
  error?: Error;
  onRetry?: () => void;
}
```

**Form Props**:
```typescript
interface FormProps {
  onSubmit: (data: FormData) => void;
  initialValues?: Partial<FormData>;
  disabled?: boolean;
}
```

---

## Styling Guidelines

### Chakra UI Theme Colors

Use semantic color tokens:
- `blue.600` - Primary brand color
- `gray.500` - Secondary text
- `gray.600` - Primary text
- `gray.200` - Borders
- `gray.50` - Background highlights
- `white` - Component backgrounds
- `red.500` - Errors

### Spacing Scale

Use Chakra's spacing scale (4px base):
- `gap={2}` - 8px
- `gap={3}` - 12px
- `gap={4}` - 16px
- `p={4}` - 16px padding
- `mb={2}` - 8px margin bottom

### Responsive Design

Use Chakra's responsive props:
```tsx
<Box
  width={{ base: '100%', md: '320px' }}
  display={{ base: 'none', md: 'block' }}
/>
```

---

## Testing Components

### Component Test Template

```tsx
import { render, screen } from '@testing-library/react';
import { Header } from './Header';

describe('Header', () => {
  it('renders app title', () => {
    render(<Header />);
    expect(screen.getByText(/Weather Vibes/i)).toBeInTheDocument();
  });

  it('toggles sidebar when hamburger clicked', () => {
    // Test implementation
  });
});
```

---

## Future Components to Add

### UI Components
- `LoadingSpinner` - Reusable loading indicator
- `ErrorBoundary` - Catch and display errors
- `Toast` - Notification system
- `Modal` - Generic modal wrapper
- `Card` - Reusable card container

### Feature-Specific
- `HeatmapLayer` - Mapbox heatmap overlay
- `LocationMarker` - Custom map markers
- `CalendarModal` - Monthly score visualization
- `RecommendationCard` - AI advisor recommendations
- `ScoreDisplay` - Visual score indicator

### Layout
- `Footer` - Bottom credits/links
- `MobileNav` - Mobile navigation drawer

---

## Component Checklist

When creating a new component:
- [ ] Add TypeScript types for props
- [ ] Document purpose and usage
- [ ] Handle loading states
- [ ] Handle error states
- [ ] Add accessibility attributes
- [ ] Make responsive
- [ ] Add to this documentation
- [ ] Write tests

---

**Last Updated**: 2025-10-04
