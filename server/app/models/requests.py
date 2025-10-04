from pydantic import BaseModel, Field
from typing import Optional


class WhereRequest(BaseModel):
    """Request model for finding the best locations for a vibe."""

    vibe: str = Field(..., description="Vibe ID (e.g., 'stargazing', 'beach_day')")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    year: Optional[int] = Field(None, description="Year for historical data")
    center_lat: float = Field(..., ge=-90, le=90, description="Center latitude")
    center_lon: float = Field(..., ge=-180, le=180, description="Center longitude")
    radius_km: float = Field(..., gt=0, le=500, description="Search radius in km")
    resolution: Optional[float] = Field(5, description="Grid resolution in km")

    class Config:
        json_schema_extra = {
            "example": {
                "vibe": "stargazing",
                "month": 7,
                "center_lat": 12.9716,
                "center_lon": 77.5946,
                "radius_km": 100,
                "resolution": 5
            }
        }


class WhenRequest(BaseModel):
    """Request model for finding the best times for a vibe at a location."""

    vibe: str = Field(..., description="Vibe ID")
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    year: Optional[int] = Field(None, description="Year for historical data")

    class Config:
        json_schema_extra = {
            "example": {
                "vibe": "beach_day",
                "lat": 12.9716,
                "lon": 77.5946
            }
        }


class AdvisorRequest(BaseModel):
    """Request model for getting specialized advisor recommendations."""

    advisor_type: str = Field(
        ...,
        description="Type of advisor: 'fashion', 'crop', or 'mood'"
    )
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    year: Optional[int] = Field(None, description="Year for historical data")
    additional_params: Optional[dict] = Field(
        None,
        description="Additional parameters specific to the advisor"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "advisor_type": "fashion",
                "lat": 12.9716,
                "lon": 77.5946,
                "month": 7,
                "additional_params": {}
            }
        }
