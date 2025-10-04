from fastapi import APIRouter, HTTPException
from app.models.requests import WhenRequest
from app.models.responses import WhenResponse, MonthlyScore
from app.core.vibe_engine import get_vibe_engine
from app.services.data_service import get_data_service

router = APIRouter()

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


@router.post("/when", response_model=WhenResponse)
async def find_when(request: WhenRequest):
    """
    Find the best months for a given vibe at a location.
    Returns monthly vibe scores.

    Args:
        request: WhenRequest containing vibe and location

    Returns:
        WhenResponse with monthly scores

    Raises:
        HTTPException: If vibe not found or no data available
    """
    try:
        vibe_engine = get_vibe_engine()
        data_service = get_data_service()

        # Get vibe configuration
        vibe_config = vibe_engine.get_vibe_config(request.vibe)
        required_params = vibe_engine.get_required_parameters(request.vibe)

        monthly_scores = []

        # Calculate score for each month
        for month in range(1, 13):
            parameter_values = data_service.get_all_parameters(
                required_params,
                request.lat,
                request.lon,
                month,
                request.year
            )

            # Skip if any required parameters are missing
            if len(parameter_values) != len(required_params):
                continue

            # Calculate vibe score
            score = vibe_engine.calculate_vibe_score(
                request.vibe,
                parameter_values
            )

            monthly_scores.append(MonthlyScore(
                month=month,
                month_name=MONTH_NAMES[month - 1],
                score=score
            ))

        if not monthly_scores:
            raise HTTPException(
                status_code=404,
                detail="No valid data found for the specified location"
            )

        # Find best and worst months
        best_month = max(monthly_scores, key=lambda x: x.score).month
        worst_month = min(monthly_scores, key=lambda x: x.score).month

        return WhenResponse(
            vibe=request.vibe,
            location={"lat": request.lat, "lon": request.lon},
            monthly_scores=monthly_scores,
            best_month=best_month,
            worst_month=worst_month,
            metadata={
                "year": request.year,
                "num_months": len(monthly_scores),
                "vibe_name": vibe_config.get("name", request.vibe)
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
