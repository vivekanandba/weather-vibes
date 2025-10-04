from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.api.router import api_router
from app.core import vibe_engine as vibe_engine_module
from app.services import data_service as data_service_module


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup: Initialize global instances
    print("=" * 50)
    print("Starting Weather Vibes API...")
    print("=" * 50)

    # Initialize vibe engine
    print("Loading vibe dictionary...")
    vibe_engine_module.vibe_engine = vibe_engine_module.VibeEngine()
    print(f"✓ Loaded {len(vibe_engine_module.vibe_engine.vibes)} vibes")

    # Initialize data service
    print(f"Initializing data service (path: {settings.data_path})...")
    data_service_module.data_service = data_service_module.DataService(
        settings.data_path
    )
    print("✓ Data service initialized")

    print("=" * 50)
    print(f"Server ready at http://{settings.host}:{settings.port}")
    print(f"API docs at http://{settings.host}:{settings.port}/docs")
    print("=" * 50)

    yield

    # Shutdown: Cleanup if needed
    print("\nShutting down Weather Vibes API...")


# Create FastAPI application
app = FastAPI(
    title="Weather Vibes API",
    description="Theme-based weather discovery engine for the Weather Vibes application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
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
    """Root endpoint with API information."""
    return {
        "message": "Weather Vibes API",
        "version": "1.0.0",
        "description": "Theme-based weather discovery engine",
        "docs": "/docs",
        "health": "/health",
        "vibes": "/vibes"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    vibe_engine = vibe_engine_module.get_vibe_engine()
    return {
        "status": "healthy",
        "vibes_loaded": len(vibe_engine.vibes),
        "data_path": settings.data_path
    }


@app.get("/vibes")
async def list_vibes():
    """List all available vibes and advisors."""
    vibe_engine = vibe_engine_module.get_vibe_engine()
    all_vibes = vibe_engine.list_vibes()

    # Separate standard vibes from advisors
    standard_vibes = [v for v in all_vibes if v["type"] == "standard"]
    advisors = [v for v in all_vibes if v["type"] == "advisor"]

    return {
        "total": len(all_vibes),
        "standard_vibes": standard_vibes,
        "advisors": advisors
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
