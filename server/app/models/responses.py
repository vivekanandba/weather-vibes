from pydantic import BaseModel
from typing import List, Optional


class LocationScore(BaseModel):
    """A single location with its vibe score."""
    lat: float
    lon: float
    score: float


class WhereResponse(BaseModel):
    """Response model for the where endpoint."""
    vibe: str
    month: int
    scores: List[LocationScore]
    max_score: float
    min_score: float
    metadata: dict


class MonthlyScore(BaseModel):
    """A single month with its vibe score."""
    month: int
    month_name: str
    score: float


class WhenResponse(BaseModel):
    """Response model for the when endpoint."""
    vibe: str
    location: dict
    monthly_scores: List[MonthlyScore]
    best_month: int
    worst_month: int
    metadata: dict


class Recommendation(BaseModel):
    """A single recommendation from an advisor."""
    item: str
    icon: str
    description: Optional[str] = None


class AdvisorResponse(BaseModel):
    """Response model for the advisor endpoint."""
    advisor_type: str
    location: dict
    recommendations: List[Recommendation]
    metadata: dict
    raw_data: Optional[dict] = None
