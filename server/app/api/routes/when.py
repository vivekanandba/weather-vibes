from fastapi import APIRouter, HTTPException
from app.models.requests import WhenRequest
from app.models.responses import WhenResponse, MonthlyScore, DailyScore, HourlyScore
from app.core.vibe_engine import get_vibe_engine
from app.services.data_service import get_data_service
from datetime import datetime, timedelta
from typing import List, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


@router.post("/when", response_model=WhenResponse)
async def find_when(request: WhenRequest):
    """
    Find the best times for a given vibe at a location.
    Returns monthly, daily, or hourly vibe scores based on analysis_type.

    Args:
        request: WhenRequest containing vibe, location, and analysis type

    Returns:
        WhenResponse with time-based scores

    Raises:
        HTTPException: If vibe not found or no data available
    """
    logger.info(f"When endpoint called with request: {request}")

    try:
        logger.info("Initializing vibe engine and data service")
        vibe_engine = get_vibe_engine()
        data_service = get_data_service()
        logger.info("Services initialized successfully")

        # Get vibe configuration
        logger.info("Getting vibe configuration")
        vibe_config = vibe_engine.get_vibe_config(request.vibe)
        required_params = vibe_engine.get_required_parameters(request.vibe)
        logger.info(f"Vibe config: {vibe_config}")
        logger.info(f"Required parameters: {required_params}")

        analysis_type = request.analysis_type or "monthly"
        logger.info(f"Analysis type: {analysis_type}")

        # Determine time parameters
        logger.info("Determining time parameters")
        if request.start_date and request.end_date:
            logger.info(f"Using date range: {request.start_date} to {request.end_date}")
            start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
            year = start_date.year
        else:
            logger.info(f"Using year: {request.year}")
            year = request.year or datetime.now().year
            start_date = None
            end_date = None

        logger.info(
            f"Final time parameters - year: {year}, start_date: {start_date}, end_date: {end_date}"
        )

        if analysis_type == "monthly":
            logger.info("Calling monthly analysis")
            return await _analyze_monthly(
                vibe_engine,
                data_service,
                request,
                vibe_config,
                required_params,
                year,
                start_date,
                end_date,
            )
        elif analysis_type == "daily":
            logger.info("Calling daily analysis")
            return await _analyze_daily(
                vibe_engine,
                data_service,
                request,
                vibe_config,
                required_params,
                year,
                start_date,
                end_date,
            )
        elif analysis_type == "hourly":
            logger.info("Calling hourly analysis")
            return await _analyze_hourly(
                vibe_engine,
                data_service,
                request,
                vibe_config,
                required_params,
                year,
                start_date,
                end_date,
            )
        else:
            logger.error(f"Invalid analysis type: {analysis_type}")
            raise HTTPException(
                status_code=400,
                detail="analysis_type must be 'monthly', 'daily', or 'hourly'",
            )

    except ValueError as e:
        logger.error(f"ValueError in when endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in when endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


async def _analyze_monthly(
    vibe_engine,
    data_service,
    request,
    vibe_config,
    required_params,
    year,
    start_date,
    end_date,
):
    """Analyze monthly scores."""
    logger.info("Starting monthly analysis")
    monthly_scores = []

    # Calculate score for each month
    logger.info("Calculating scores for each month")
    for month in range(1, 13):
        logger.debug(f"Processing month {month}")

        try:
            parameter_values = data_service.get_all_parameters(
                required_params,
                request.lat,
                request.lon,
                month,
                year,
                start_date,
                end_date,
            )
            logger.debug(f"Parameter values for month {month}: {parameter_values}")

            # Skip if any required parameters are missing
            if len(parameter_values) != len(required_params):
                logger.warning(
                    f"Skipping month {month}: Missing parameters. Got {len(parameter_values)}, expected {len(required_params)}"
                )
                continue

            # Calculate vibe score
            score = vibe_engine.calculate_vibe_score(request.vibe, parameter_values)
            logger.debug(f"Calculated score for month {month}: {score}")

            monthly_scores.append(
                MonthlyScore(
                    month=month, month_name=MONTH_NAMES[month - 1], score=score
                )
            )
        except Exception as e:
            logger.error(f"Error processing month {month}: {str(e)}")
            continue

    logger.info(f"Monthly analysis completed. Generated {len(monthly_scores)} scores")

    if not monthly_scores:
        logger.error("No monthly scores calculated")
        raise HTTPException(
            status_code=404, detail="No valid data found for the specified location"
        )

    # Find best and worst months
    logger.info("Finding best and worst months")
    best_month = max(monthly_scores, key=lambda x: x.score).month
    worst_month = min(monthly_scores, key=lambda x: x.score).month
    logger.info(f"Best month: {best_month}, Worst month: {worst_month}")

    metadata = {
        "year": year,
        "num_months": len(monthly_scores),
        "vibe_name": vibe_config.get("name", request.vibe),
    }

    if start_date and end_date:
        metadata["date_range"] = {"start": request.start_date, "end": request.end_date}

    logger.info("Creating monthly response")
    response = WhenResponse(
        vibe=request.vibe,
        location={"lat": request.lat, "lon": request.lon},
        monthly_scores=monthly_scores,
        best_month=best_month,
        worst_month=worst_month,
        analysis_type="monthly",
        metadata=metadata,
    )

    logger.info("Monthly analysis completed successfully")
    return response


async def _analyze_daily(
    vibe_engine,
    data_service,
    request,
    vibe_config,
    required_params,
    year,
    start_date,
    end_date,
):
    """Analyze daily scores within a date range."""
    if not start_date or not end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date and end_date are required for daily analysis",
        )

    daily_scores = []
    current_date = start_date

    while current_date <= end_date:
        # Get parameter values for this specific date
        parameter_values = data_service.get_all_parameters(
            required_params,
            request.lat,
            request.lon,
            current_date.month,
            year,
            current_date,
            current_date,
        )

        if len(parameter_values) == len(required_params):
            score = vibe_engine.calculate_vibe_score(request.vibe, parameter_values)

            daily_scores.append(
                DailyScore(date=current_date.strftime("%Y-%m-%d"), score=score)
            )

        current_date += timedelta(days=1)

    if not daily_scores:
        raise HTTPException(
            status_code=404, detail="No valid data found for the specified date range"
        )

    # Find best and worst dates
    best_date = max(daily_scores, key=lambda x: x.score).date
    worst_date = min(daily_scores, key=lambda x: x.score).date

    metadata = {
        "year": year,
        "num_days": len(daily_scores),
        "vibe_name": vibe_config.get("name", request.vibe),
        "date_range": {"start": request.start_date, "end": request.end_date},
    }

    return WhenResponse(
        vibe=request.vibe,
        location={"lat": request.lat, "lon": request.lon},
        daily_scores=daily_scores,
        best_date=best_date,
        worst_date=worst_date,
        analysis_type="daily",
        metadata=metadata,
    )


async def _analyze_hourly(
    vibe_engine,
    data_service,
    request,
    vibe_config,
    required_params,
    year,
    start_date,
    end_date,
):
    """Analyze hourly scores for a specific date."""
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if not end_date:
        end_date = start_date

    hourly_scores = []

    # For hourly analysis, we'll simulate hourly data based on daily patterns
    # In a real implementation, you'd have hourly weather data
    for hour in range(24):
        # Simulate hourly variation (this is a simplified approach)
        base_score = vibe_engine.calculate_vibe_score(
            request.vibe,
            data_service.get_all_parameters(
                required_params,
                request.lat,
                request.lon,
                start_date.month,
                year,
                start_date,
                end_date,
            ),
        )

        # Add hourly variation based on typical patterns
        if 6 <= hour <= 8:  # Morning
            score = base_score * 0.9
        elif 9 <= hour <= 11:  # Late morning
            score = base_score * 1.1
        elif 12 <= hour <= 14:  # Midday
            score = base_score * 1.2
        elif 15 <= hour <= 17:  # Afternoon
            score = base_score * 1.1
        elif 18 <= hour <= 20:  # Evening
            score = base_score * 0.8
        else:  # Night
            score = base_score * 0.6

        hourly_scores.append(
            HourlyScore(hour=hour, score=max(0, min(100, score)))  # Clamp between 0-100
        )

    # Find best and worst hours
    best_hour = max(hourly_scores, key=lambda x: x.score).hour
    worst_hour = min(hourly_scores, key=lambda x: x.score).hour

    metadata = {
        "year": year,
        "num_hours": len(hourly_scores),
        "vibe_name": vibe_config.get("name", request.vibe),
        "date_range": {
            "start": request.start_date or start_date.strftime("%Y-%m-%d"),
            "end": request.end_date or end_date.strftime("%Y-%m-%d"),
        },
    }

    return WhenResponse(
        vibe=request.vibe,
        location={"lat": request.lat, "lon": request.lon},
        hourly_scores=hourly_scores,
        best_hour=best_hour,
        worst_hour=worst_hour,
        analysis_type="hourly",
        metadata=metadata,
    )
