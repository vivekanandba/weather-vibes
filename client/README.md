# Weather Vibes - Client Application

A Next.js 14 application for theme-based weather discovery powered by NASA POWER data.

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Mapbox account (for map visualization)

### Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env.local
```

2. Get your Mapbox token from [https://account.mapbox.com/](https://account.mapbox.com/)

3. Update `.env.local` with your Mapbox token:
```
NEXT_PUBLIC_MAPBOX_TOKEN=your_actual_mapbox_token
```

### Installation

```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
client/
├── src/
│   ├── app/                    # Next.js 14 app directory
│   │   ├── layout.tsx         # Root layout with providers
│   │   ├── page.tsx           # Main map view page
│   │   └── providers.tsx      # Client-side providers
│   ├── components/
│   │   ├── layout/            # Header, Sidebar
│   │   ├── map/               # MapView with Mapbox
│   │   ├── vibe/              # VibeSelector
│   │   └── features/          # Where, When, Advisors panels
│   ├── stores/                # Zustand state management
│   ├── services/              # API client services
│   ├── types/                 # TypeScript types
│   ├── utils/                 # Helper functions
│   ├── config/                # App configuration
│   └── hooks/                 # Custom React hooks
└── public/                    # Static assets
```

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **UI Library**: Chakra UI v2
- **State Management**: Zustand
- **Map Library**: Mapbox GL JS + react-map-gl
- **API Client**: Axios + React Query
- **Styling**: Tailwind CSS + Chakra UI

## Features

### 1. Where Feature
Find the best locations for your selected vibe based on historical weather data.

### 2. When Feature
Find the best times (months) for your vibe at a specific location.

### 3. AI Advisors
Get personalized recommendations:
- **Fashion Stylist**: Weather-appropriate outfit suggestions
- **Crop Advisor**: Optimal planting and growing conditions
- **Mood Predictor**: Wellness suggestions based on weather

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Configuration

### Vibes Dictionary

All vibes are configured in `src/config/vibes.ts`. You can add or modify vibes by editing this file.

### Mapbox Configuration

Mapbox settings are in `src/config/mapbox.ts`. You can change the default map style, center location, and zoom level.

### Theme Customization

Chakra UI theme is configured in `src/config/theme.ts`.

## API Integration

The app is designed to work with a FastAPI backend. API services are located in `src/services/`:

- `whereService.ts` - Location-based queries
- `whenService.ts` - Time-based queries
- `advisorService.ts` - AI advisor recommendations

Update `NEXT_PUBLIC_API_BASE_URL` in `.env.local` to point to your backend.

## Next Steps

1. ✅ Basic framework is set up
2. 🚧 Integrate backend API calls
3. 🚧 Implement heatmap visualization for "Where" feature
4. 🚧 Add calendar modal for "When" feature
5. 🚧 Build recommendation cards for "Advisors" feature
6. 🚧 Add loading states and error handling
7. 🚧 Implement responsive design for mobile

## Development Notes

- All components use TypeScript with strict mode
- State management is handled by Zustand stores
- API calls are cached using React Query
- Mapbox token is required for map functionality

## Team Responsibilities

- **Bhawesh**: UI/UX, Mapbox integration, shared components
- **Vivek**: "Where" feature (backend + frontend heatmap)
- **Kiran**: "Advisors" feature (backend + frontend cards)

## Troubleshooting

### Map not loading
- Ensure `NEXT_PUBLIC_MAPBOX_TOKEN` is set in `.env.local`
- Check browser console for errors
- Verify Mapbox token is valid

### API errors
- Ensure backend is running on the correct port
- Check `NEXT_PUBLIC_API_BASE_URL` in `.env.local`
- Verify CORS is configured on backend
<!-- Test frontend deployment -->
