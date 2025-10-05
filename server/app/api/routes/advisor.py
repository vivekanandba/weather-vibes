from fastapi import APIRouter, HTTPException
from app.models.requests import AdvisorRequest
from app.models.responses import AdvisorResponse
from app.core.vibe_engine import get_vibe_engine
from app.services.data_service import get_data_service
from app.core.advisors import crop_advisor, mood_predictor
from app.core.advisors.fashion_rules import fashion_rules
from typing import List
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

ADVISOR_FUNCTIONS = {
    "fashion": fashion_rules.generate_recommendations,
    "crop": crop_advisor.generate_recommendations,
    "mood": mood_predictor.generate_recommendations,
}

ADVISOR_VIBE_KEYS = {
    "fashion": "fashion_stylist",
    "crop": "crop_advisor",
    "mood": "mood_predictor",
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
    logger.info(f"Advisor endpoint called with request: {request}")

    try:
        # Validate advisor type
        logger.info(f"Validating advisor type: {request.advisor_type}")
        if request.advisor_type not in ADVISOR_FUNCTIONS:
            logger.error(f"Invalid advisor type: {request.advisor_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Unknown advisor type: {request.advisor_type}. "
                f"Available types: {list(ADVISOR_FUNCTIONS.keys())}",
            )

        logger.info("Initializing services")
        vibe_engine = get_vibe_engine()
        data_service = get_data_service()
        logger.info("Services initialized successfully")

        # Get advisor configuration
        logger.info("Getting advisor configuration")
        advisor_key = ADVISOR_VIBE_KEYS[request.advisor_type]
        logger.info(f"Advisor key: {advisor_key}")

        try:
            vibe_config = vibe_engine.get_vibe_config(advisor_key)
            logger.info(f"Vibe config: {vibe_config}")
        except Exception as e:
            logger.error(f"Error getting vibe config for {advisor_key}: {str(e)}")
            raise HTTPException(
                status_code=400, detail=f"Invalid advisor configuration: {str(e)}"
            )

        required_params = vibe_config["parameters"]
        logger.info(f"Required parameters: {required_params}")

        # Get parameter values
        logger.info("Getting parameter values")
        try:
            parameter_values = data_service.get_all_parameters(
                required_params, request.lat, request.lon, request.month, request.year
            )
            logger.info(f"Parameter values retrieved: {parameter_values}")
        except Exception as e:
            logger.error(f"Error getting parameter values: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Error retrieving weather data: {str(e)}"
            )

        if not parameter_values:
            logger.error("No parameter values found")
            raise HTTPException(
                status_code=404, detail="No data available for the specified location"
            )

        # Get advisor function and generate recommendations
        logger.info("Generating recommendations")
        advisor_func = ADVISOR_FUNCTIONS[request.advisor_type]
        logger.info(f"Using advisor function: {advisor_func}")

        try:
            advisor_result = advisor_func(
                parameter_values, request.additional_params or {}
            )
            logger.info(f"Generated advisor result: {type(advisor_result)}")
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Error generating recommendations: {str(e)}"
            )

        # Transform advisor result to list of recommendations
        recommendations = _transform_advisor_result_to_recommendations(advisor_result, request.advisor_type)
        logger.info(f"Transformed to {len(recommendations)} recommendations")

        logger.info("Creating response")
        response = AdvisorResponse(
            advisor_type=request.advisor_type,
            location={"lat": request.lat, "lon": request.lon},
            recommendations=recommendations,
            metadata={
                "month": request.month,
                "year": request.year,
                "advisor_name": vibe_config.get("name", request.advisor_type),
            },
            raw_data=parameter_values,
        )

        logger.info(
            f"Advisor endpoint completed successfully. Returning {len(recommendations)} recommendations"
        )
        return response

    except ValueError as e:
        logger.error(f"ValueError in advisor endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in advisor endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


def _transform_advisor_result_to_recommendations(advisor_result: dict, advisor_type: str) -> List[dict]:
    """
    Transform advisor result to list of Recommendation objects.
    
    Args:
        advisor_result: The result from the advisor function
        advisor_type: The type of advisor (fashion, crop, mood)
        
    Returns:
        List of recommendation dictionaries
    """
    from app.models.responses import Recommendation
    
    recommendations = []
    
    if advisor_type == "fashion":
        # Transform fashion advisor result
        if "outfit_recommendations" in advisor_result:
            for outfit in advisor_result["outfit_recommendations"]:
                recommendations.append(Recommendation(
                    item=outfit.get("name", "Outfit"),
                    icon="👕",
                    description=f"Comfort: {outfit.get('comfort_score', 0)}/100, Style: {outfit.get('style_score', 0)}/100"
                ))
        
        if "accessory_recommendations" in advisor_result:
            for accessory in advisor_result["accessory_recommendations"]:
                recommendations.append(Recommendation(
                    item=accessory.get("name", "Accessory"),
                    icon="🎒",
                    description=accessory.get("reason", "")
                ))
    
    elif advisor_type == "crop":
        # Transform crop advisor result
        if "alerts" in advisor_result:
            for alert in advisor_result["alerts"]:
                recommendations.append(Recommendation(
                    item=alert.get("message", "Alert"),
                    icon="⚠️",
                    description=f"Priority: {alert.get('priority', 'medium')}"
                ))
        
        if "actionable_recommendations" in advisor_result:
            for rec in advisor_result["actionable_recommendations"]:
                recommendations.append(Recommendation(
                    item=rec.get("title", "Recommendation"),
                    icon="🌱",
                    description=rec.get("description", "")
                ))
    
    elif advisor_type == "mood":
        # Transform mood advisor result
        if "activity_suggestions" in advisor_result:
            for activity in advisor_result["activity_suggestions"]:
                recommendations.append(Recommendation(
                    item=activity.get("name", "Activity"),
                    icon="🎯",
                    description=f"Suitability: {activity.get('suitability', 'medium')}"
                ))
        
        if "wellness_suggestions" in advisor_result:
            for suggestion in advisor_result["wellness_suggestions"]:
                recommendations.append(Recommendation(
                    item=suggestion,
                    icon="💡",
                    description="Wellness tip"
                ))
    
    # If no specific recommendations found, create generic ones
    if not recommendations:
        recommendations.append(Recommendation(
            item="Weather Analysis Complete",
            icon="✅",
            description="Analysis completed successfully"
        ))
    
    return recommendations
