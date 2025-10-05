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
    month: Optional[int] = None
    year: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    scores: List[LocationScore]
    max_score: float
    min_score: float
    metadata: dict


class MonthlyScore(BaseModel):
    """A single month with its vibe score."""

    month: int
    month_name: str
    score: float


class DailyScore(BaseModel):
    """A single day with its vibe score."""

    date: str  # YYYY-MM-DD format
    score: float


class HourlyScore(BaseModel):
    """A single hour with its vibe score."""

    hour: int
    score: float


class WhenResponse(BaseModel):
    """Response model for the when endpoint."""

    vibe: str
    location: dict
    monthly_scores: Optional[List[MonthlyScore]] = None
    daily_scores: Optional[List[DailyScore]] = None
    hourly_scores: Optional[List[HourlyScore]] = None
    best_month: Optional[int] = None
    worst_month: Optional[int] = None
    best_date: Optional[str] = None
    worst_date: Optional[str] = None
    best_hour: Optional[int] = None
    worst_hour: Optional[int] = None
    analysis_type: str
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
