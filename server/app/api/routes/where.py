from fastapi import APIRouter, HTTPException
from app.models.requests import WhereRequest
from app.models.responses import WhereResponse, LocationScore
from app.core.vibe_engine import get_vibe_engine
from app.services.data_service import get_data_service

router = APIRouter()


@router.post("/where", response_model=WhereResponse)
async def find_where(request: WhereRequest):
    """
    Find the best locations for a given vibe within a radius.
    Returns a heatmap of vibe scores.

    Args:
        request: WhereRequest containing vibe, location, radius, and time

    Returns:
        WhereResponse with scored grid of locations

    Raises:
        HTTPException: If vibe not found or no data available
    """
    try:
        vibe_engine = get_vibe_engine()
        data_service = get_data_service()

        # Get vibe configuration
        vibe_config = vibe_engine.get_vibe_config(request.vibe)
        required_params = vibe_engine.get_required_parameters(request.vibe)

        # Get values in radius for each parameter
        scores = []

        # First, collect all unique grid points
        first_param = required_params[0]
        grid_data = data_service.get_values_in_radius(
            first_param,
            request.center_lat,
            request.center_lon,
            request.radius_km,
            request.month,
            request.resolution,
            request.year
        )

        # For each grid point, get all parameter values and calculate score
        for lat, lon, _ in grid_data:
            parameter_values = data_service.get_all_parameters(
                required_params,
                lat,
                lon,
                request.month,
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

            scores.append(LocationScore(lat=lat, lon=lon, score=score))

        if not scores:
            raise HTTPException(
                status_code=404,
                detail="No valid data found in the specified area"
            )

        # Calculate statistics
        score_values = [s.score for s in scores]
        max_score = max(score_values)
        min_score = min(score_values)

        return WhereResponse(
            vibe=request.vibe,
            month=request.month,
            scores=scores,
            max_score=max_score,
            min_score=min_score,
            metadata={
                "center": {"lat": request.center_lat, "lon": request.center_lon},
                "radius_km": request.radius_km,
                "resolution_km": request.resolution,
                "num_points": len(scores),
                "vibe_name": vibe_config.get("name", request.vibe)
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
