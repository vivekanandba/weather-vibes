from fastapi import APIRouter, HTTPException
from app.models.requests import AdvisorRequest
from app.models.responses import AdvisorResponse
from app.core.vibe_engine import get_vibe_engine
from app.services.data_service import get_data_service
from app.core.advisors import fashion_rules, crop_advisor, mood_predictor

router = APIRouter()

ADVISOR_FUNCTIONS = {
    "fashion": fashion_rules.generate_recommendations,
    "crop": crop_advisor.generate_recommendations,
    "mood": mood_predictor.generate_recommendations
}

ADVISOR_VIBE_KEYS = {
    "fashion": "fashion_stylist",
    "crop": "crop_advisor",
    "mood": "mood_predictor"
}


@router.post("/advisor", response_model=AdvisorResponse)
async def get_advisor_recommendations(request: AdvisorRequest):
    """
    Get specialized recommendations from an advisor.

    Args:
        request: AdvisorRequest with advisor type, location, and time

    Returns:
        AdvisorResponse with personalized recommendations

    Raises:
        HTTPException: If advisor type invalid or no data available
    """
    try:
        # Validate advisor type
        if request.advisor_type not in ADVISOR_FUNCTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown advisor type: {request.advisor_type}. "
                       f"Available types: {list(ADVISOR_FUNCTIONS.keys())}"
            )

        vibe_engine = get_vibe_engine()
        data_service = get_data_service()

        # Get advisor configuration
        advisor_key = ADVISOR_VIBE_KEYS[request.advisor_type]
        vibe_config = vibe_engine.get_vibe_config(advisor_key)
        required_params = vibe_config["parameters"]

        # Get parameter values
        parameter_values = data_service.get_all_parameters(
            required_params,
            request.lat,
            request.lon,
            request.month,
            request.year
        )

        if not parameter_values:
            raise HTTPException(
                status_code=404,
                detail="No data available for the specified location"
            )

        # Get advisor function and generate recommendations
        advisor_func = ADVISOR_FUNCTIONS[request.advisor_type]
        recommendations = advisor_func(
            parameter_values,
            request.additional_params or {}
        )

        return AdvisorResponse(
            advisor_type=request.advisor_type,
            location={"lat": request.lat, "lon": request.lon},
            recommendations=recommendations,
            metadata={
                "month": request.month,
                "year": request.year,
                "advisor_name": vibe_config.get("name", request.advisor_type)
            },
            raw_data=parameter_values
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
