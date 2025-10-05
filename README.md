# Weather Vibes 🌤️

**Weather Vibes** is an intuitive, theme-based weather discovery engine that closes the gap between what people want to do and when and where is the best time to do it. Built for the NASA Space Apps Challenge 2025.

## 🎯 Project Overview

Weather Vibes helps users discover the perfect weather conditions for their desired activities by combining NASA weather data with intelligent recommendations. Whether you're planning a beach day, hiking trip, or outdoor photography session, Weather Vibes tells you the best time and place to go.

## 🏗️ Architecture

This is a full-stack application with three main components:

### 📱 **Frontend (Next.js)**
- **Location:** `client/`
- **Tech Stack:** Next.js 15, React 19, TypeScript, Chakra UI, Mapbox GL
- **Features:** Interactive maps, vibe selection, weather visualization, location search

### 🚀 **Backend (FastAPI)**
- **Location:** `server/`
- **Tech Stack:** FastAPI, Python, Pydantic, Rasterio, GeoPandas
- **Features:** Weather data processing, vibe scoring, geospatial analysis, API endpoints

### 📊 **Data Pipeline**
- **Location:** `data/`
- **Tech Stack:** Python, NASA POWER API, GeoTIFF processing
- **Features:** Weather data aggregation, point-of-interest analysis, offline data packs

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)
- Git

### Frontend Setup
```bash
cd client
npm install
npm run dev
```

### Backend Setup
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Data Pipeline Setup
```bash
cd data
pip install -r requirements.txt
python cron_job.py
```

## 📁 Project Structure

```
weather-vibes/
├── client/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   ├── stores/        # Zustand state management
│   │   └── types/         # TypeScript definitions
│   └── package.json
├── server/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Business logic
│   │   ├── models/        # Pydantic models
│   │   └── services/      # Service layer
│   └── requirements.txt
├── data/                   # Data pipeline and processing
│   ├── pipeline/          # Data processing scripts
│   ├── outputs/           # Processed weather data
│   └── config/           # Configuration files
├── docs/                   # Comprehensive documentation
│   ├── SPEC.md            # Technical specifications
│   ├── DESIGN.md          # System design
│   ├── PLAN.md            # Project planning
│   └── README.md          # Documentation guide
└── poc/                    # Proof of concept notebooks
```

## 🎨 Key Features

### 🌍 **Interactive Weather Maps**
- Real-time weather visualization using Mapbox GL
- Custom weather layers and overlays
- Interactive point-of-interest markers

### 🎯 **Vibe-Based Discovery**
- Pre-defined activity vibes (beach, hiking, photography, etc.)
- Intelligent scoring based on weather conditions
- Personalized recommendations

### 📊 **Data-Driven Insights**
- NASA POWER API integration
- Historical weather analysis
- Predictive weather patterns

### 🗺️ **Location Intelligence**
- Geospatial analysis of weather conditions
- Point-of-interest recommendations
- Travel time and accessibility considerations

## 🛠️ Development

### Frontend Development
- **Framework:** Next.js 15 with App Router
- **UI Library:** Chakra UI with custom components
- **State Management:** Zustand for global state
- **Maps:** Mapbox GL JS for interactive maps
- **Styling:** Tailwind CSS with Chakra UI

### Backend Development
- **Framework:** FastAPI with automatic API documentation
- **Data Processing:** Rasterio for GeoTIFF files
- **Geospatial:** GeoPandas for spatial analysis
- **Caching:** Redis for performance optimization

### Data Pipeline
- **Data Source:** NASA POWER API
- **Processing:** Python scripts for data aggregation
- **Storage:** CSV and Parquet formats
- **Scheduling:** Cron jobs for automated updates

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[SPEC.md](docs/SPEC.md)** - Technical specifications and requirements
- **[DESIGN.md](docs/DESIGN.md)** - System architecture and design patterns
- **[PLAN.md](docs/PLAN.md)** - Project planning and progress tracking
- **[README.md](docs/README.md)** - Documentation guide and usage

## 🚀 Deployment

### Frontend
- Deploy to Vercel or Netlify
- Environment variables for API endpoints
- Mapbox API key configuration

### Backend
- Deploy to Railway, Render, or AWS
- Environment variables for database and API keys
- Docker containerization support

### Data Pipeline
- Scheduled cron jobs for data updates
- Cloud storage for processed data
- Monitoring and alerting setup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 NASA Space Apps Challenge 2025

This project is developed for the NASA Space Apps Challenge 2025, focusing on leveraging NASA's weather data to create innovative solutions for weather-based activity planning.

## 📞 Support

For questions or support:
- Check the [documentation](docs/README.md)
- Open an issue on GitHub
- Contact the development team

---

**Built with ❤️ for the NASA Space Apps Challenge 2025**
