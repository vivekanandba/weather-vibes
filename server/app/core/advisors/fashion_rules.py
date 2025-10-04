from typing import Dict, List
from app.models.responses import Recommendation


def generate_recommendations(
    parameters: Dict[str, float],
    additional_params: Dict
) -> List[Recommendation]:
    """
    Generate fashion recommendations based on weather parameters.

    Args:
        parameters: Dictionary of weather parameter values
        additional_params: Additional user preferences

    Returns:
        List of fashion recommendations
    """
    recommendations = []

    temp = parameters.get("T2M", 20)  # Temperature in Celsius
    sunshine = parameters.get("ALLSKY_SFC_SW_DWN", 0)  # kW-hr/m^2/day
    precipitation = parameters.get("PRECTOTCORR", 0)  # mm/day
    wind_speed = parameters.get("WS2M", 0)  # m/s

    # Temperature-based recommendations
    if temp > 30:
        recommendations.append(Recommendation(
            item="Light Cotton T-Shirt",
            icon="👕",
            description="Stay cool in breathable fabrics"
        ))
        recommendations.append(Recommendation(
            item="Shorts",
            icon="🩳",
            description="Perfect for hot weather"
        ))
    elif temp > 25:
        recommendations.append(Recommendation(
            item="Linen Shirt",
            icon="👔",
            description="Breathable and stylish"
        ))
    elif temp > 18:
        recommendations.append(Recommendation(
            item="Light Sweater",
            icon="🧥",
            description="Comfortable for mild weather"
        ))
    elif temp > 10:
        recommendations.append(Recommendation(
            item="Jacket",
            icon="🧥",
            description="Stay warm in cooler temperatures"
        ))
    else:
        recommendations.append(Recommendation(
            item="Winter Coat",
            icon="🧥",
            description="Bundle up for cold weather"
        ))

    # Sun protection
    if sunshine > 5:
        recommendations.append(Recommendation(
            item="Sunglasses",
            icon="🕶️",
            description="Protect your eyes from bright sun"
        ))
        recommendations.append(Recommendation(
            item="Sun Hat",
            icon="🧢",
            description="Shield your face from UV rays"
        ))

    # Rain protection
    if precipitation > 5:
        recommendations.append(Recommendation(
            item="Waterproof Jacket",
            icon="🧥",
            description="Stay dry in rainy conditions"
        ))
        recommendations.append(Recommendation(
            item="Umbrella",
            icon="☔",
            description="Essential for rain protection"
        ))
    elif precipitation > 1:
        recommendations.append(Recommendation(
            item="Light Rain Jacket",
            icon="🧥",
            description="Protection from light showers"
        ))

    # Wind protection
    if wind_speed > 10:
        recommendations.append(Recommendation(
            item="Windbreaker",
            icon="🧥",
            description="Block strong winds"
        ))

    return recommendations
