from fastapi import APIRouter, HTTPException
from app.models.requests import WhereRequest
from app.models.responses import WhereResponse, LocationScore
from app.core.vibe_engine import get_vibe_engine
from app.services.data_service import get_data_service
from datetime import datetime
from typing import Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

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
    logger.info(f"Where endpoint called with request: {request}")

    try:
        logger.info("Initializing vibe engine and data service")
        vibe_engine = get_vibe_engine()
        data_service = get_data_service()
        logger.info("Services initialized successfully")

        # Validate date parameters
        logger.info("Validating date parameters")
        if not request.month and not (request.start_date and request.end_date):
            logger.error("Validation failed: Neither month nor date range provided")
            raise HTTPException(
                status_code=400,
                detail="Either month or start_date/end_date must be provided",
            )

        logger.info("Getting vibe configuration")
        # Get vibe configuration
        vibe_config = vibe_engine.get_vibe_config(request.vibe)
        required_params = vibe_engine.get_required_parameters(request.vibe)
        logger.info(f"Vibe config: {vibe_config}")
        logger.info(f"Required parameters: {required_params}")

        # Determine time parameters
        logger.info("Determining time parameters")
        if request.start_date and request.end_date:
            # Date range mode
            logger.info(
                f"Using date range mode: {request.start_date} to {request.end_date}"
            )
            start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
            month = None
            year = start_date.year
        else:
            # Single month mode
            logger.info(f"Using single month mode: {request.month}")
            month = request.month
            year = request.year or datetime.now().year
            start_date = None
            end_date = None

        logger.info(
            f"Final time parameters - month: {month}, year: {year}, start_date: {start_date}, end_date: {end_date}"
        )

        # Get values in radius for each parameter
        scores = []

        # First, collect all unique grid points
        logger.info("Getting grid data for first parameter")
        first_param = required_params[0]
        logger.info(f"First parameter: {first_param}")

        try:
            grid_data = data_service.get_values_in_radius(
                first_param,
                request.center_lat,
                request.center_lon,
                request.radius_km,
                month,
                request.resolution,
                year,
                start_date,
                end_date,
            )
            logger.info(f"Grid data retrieved: {len(grid_data)} points")
        except Exception as e:
            logger.error(f"Error getting grid data: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Error getting grid data: {str(e)}"
            )

        # For each grid point, get all parameter values and calculate score
        logger.info("Processing grid points")
        for i, (lat, lon, _) in enumerate(grid_data):
            logger.debug(f"Processing point {i+1}/{len(grid_data)}: ({lat}, {lon})")

            try:
                parameter_values = data_service.get_all_parameters(
                    required_params, lat, lon, month, year, start_date, end_date
                )
                logger.debug(f"Parameter values for point {i+1}: {parameter_values}")

                # Skip if any required parameters are missing
                if len(parameter_values) != len(required_params):
                    logger.warning(
                        f"Skipping point {i+1}: Missing parameters. Got {len(parameter_values)}, expected {len(required_params)}"
                    )
                    continue

                # Calculate vibe score
                score = vibe_engine.calculate_vibe_score(request.vibe, parameter_values)
                logger.debug(f"Calculated score for point {i+1}: {score}")

                scores.append(LocationScore(lat=lat, lon=lon, score=score))
            except Exception as e:
                logger.error(f"Error processing point {i+1} ({lat}, {lon}): {str(e)}")
                continue

        logger.info(f"Processed {len(scores)} valid scores")

        if not scores:
            logger.error("No valid scores calculated")
            raise HTTPException(
                status_code=404, detail="No valid data found in the specified area"
            )

        # Calculate statistics
        logger.info("Calculating statistics")
        score_values = [s.score for s in scores]
        max_score = max(score_values)
        min_score = min(score_values)
        logger.info(f"Score range: {min_score} - {max_score}")

        # Build metadata
        logger.info("Building metadata")
        metadata = {
            "center": {"lat": request.center_lat, "lon": request.center_lon},
            "radius_km": request.radius_km,
            "resolution_km": request.resolution,
            "num_points": len(scores),
            "vibe_name": vibe_config.get("name", request.vibe),
        }

        # Add date range information if applicable
        if start_date and end_date:
            metadata["date_range"] = {
                "start": request.start_date,
                "end": request.end_date,
            }

        logger.info("Creating response")
        response = WhereResponse(
            vibe=request.vibe,
            month=month,
            year=year,
            start_date=request.start_date,
            end_date=request.end_date,
            scores=scores,
            max_score=max_score,
            min_score=min_score,
            metadata=metadata,
        )

        logger.info(
            f"Where endpoint completed successfully. Returning {len(scores)} locations"
        )
        return response

    except ValueError as e:
        logger.error(f"ValueError in where endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in where endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
