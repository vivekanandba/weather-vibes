from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.api.router import api_router
from app.core import vibe_engine as vibe_engine_module
from app.services import data_service as data_service_module
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("weather_vibes.log"),
    ],
)

# Set specific loggers to DEBUG for detailed debugging
logging.getLogger("app.api.routes.where").setLevel(logging.DEBUG)
logging.getLogger("app.api.routes.when").setLevel(logging.DEBUG)
logging.getLogger("app.api.routes.advisor").setLevel(logging.DEBUG)
logging.getLogger("app.services.data_service").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup: Initialize global instances
    logger.info("=" * 50)
    logger.info("Starting Weather Vibes API...")
    logger.info("=" * 50)

    # Initialize vibe engine
    logger.info("Loading vibe dictionary...")
    try:
        vibe_engine_module.vibe_engine = vibe_engine_module.VibeEngine()
        logger.info(f"✓ Loaded {len(vibe_engine_module.vibe_engine.vibes)} vibes")
    except Exception as e:
        logger.error(f"Failed to initialize vibe engine: {e}")
        raise

    # Initialize data service
    logger.info(f"Initializing data service (path: {settings.data_path})...")
    try:
        data_service_module.data_service = data_service_module.DataService(
            settings.data_path
        )
        logger.info("✓ Data service initialized")
    except Exception as e:
        logger.error(f"Failed to initialize data service: {e}")
        raise

    logger.info("=" * 50)
    logger.info(f"Server ready at http://{settings.host}:{settings.port}")
    logger.info(f"API docs at http://{settings.host}:{settings.port}/docs")
    logger.info("=" * 50)

    yield

    # Shutdown: Cleanup if needed
    logger.info("Shutting down Weather Vibes API...")


# Create FastAPI application
app = FastAPI(
    title="Weather Vibes API",
    description="Theme-based weather discovery engine for the Weather Vibes application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
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
    logger.info("Root endpoint accessed")
    return {
        "message": "Weather Vibes API",
        "version": "1.0.0",
        "description": "Theme-based weather discovery engine",
        "docs": "/docs",
        "health": "/health",
        "vibes": "/vibes",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check endpoint accessed")
    try:
        vibe_engine = vibe_engine_module.get_vibe_engine()
        return {
            "status": "healthy",
            "vibes_loaded": len(vibe_engine.vibes),
            "data_path": settings.data_path,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


@app.get("/vibes")
async def list_vibes():
    """List all available vibes and advisors."""
    logger.info("Vibes endpoint accessed")
    try:
        vibe_engine = vibe_engine_module.get_vibe_engine()
        all_vibes = vibe_engine.list_vibes()

        # Separate standard vibes from advisors
        standard_vibes = [v for v in all_vibes if v["type"] == "standard"]
        advisors = [v for v in all_vibes if v["type"] == "advisor"]

        return {
            "total": len(all_vibes),
            "standard_vibes": standard_vibes,
            "advisors": advisors,
        }
    except Exception as e:
        logger.error(f"Failed to list vibes: {e}")
        raise


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host=settings.host, port=settings.port, reload=settings.debug
    )
