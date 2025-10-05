from fastapi import APIRouter
from app.api.routes import where, when, advisor, debug

# Create main API router
api_router = APIRouter()

# Include route modules
api_router.include_router(where.router, tags=["where"])
api_router.include_router(when.router, tags=["when"])
api_router.include_router(advisor.router, tags=["advisor"])
api_router.include_router(debug.router, tags=["debug"])
