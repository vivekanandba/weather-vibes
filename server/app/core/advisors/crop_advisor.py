from typing import Dict, List
from app.models.responses import Recommendation


def generate_recommendations(
    parameters: Dict[str, float],
    additional_params: Dict
) -> List[Recommendation]:
    """
    Generate crop and farming recommendations.

    Args:
        parameters: Dictionary of weather parameter values
        additional_params: Additional farming parameters (e.g., crop_type)

    Returns:
        List of farming recommendations
    """
    recommendations = []

    temp = parameters.get("T2M", 20)
    precipitation = parameters.get("PRECTOTCORR", 0)
    temp_min = parameters.get("T2M_MIN", temp - 5)
    temp_max = parameters.get("T2M_MAX", temp + 5)
    humidity = parameters.get("RH2M", 50)

    # Frost alert
    if temp_min < 2:
        recommendations.append(Recommendation(
            item="Frost Alert",
            icon="❄️",
            description=f"Risk of frost (min temp: {temp_min:.1f}°C). Protect sensitive crops."
        ))

    # Optimal planting conditions
    if 15 <= temp <= 25 and 20 <= precipitation <= 50:
        recommendations.append(Recommendation(
            item="Optimal Planting Window",
            icon="🌱",
            description="Excellent conditions for planting most crops"
        ))

    # Drought warning
    if precipitation < 5:
        recommendations.append(Recommendation(
            item="Drought Warning",
            icon="🏜️",
            description="Low rainfall. Consider irrigation."
        ))

    # Heavy rain warning
    if precipitation > 100:
        recommendations.append(Recommendation(
            item="Heavy Rain Alert",
            icon="🌧️",
            description="Excessive rainfall may cause waterlogging"
        ))

    # Heat stress warning
    if temp_max > 35:
        recommendations.append(Recommendation(
            item="Heat Stress Warning",
            icon="🌡️",
            description=f"High temperatures (max: {temp_max:.1f}°C). Ensure adequate irrigation."
        ))

    # Humidity-related recommendations
    if humidity > 80:
        recommendations.append(Recommendation(
            item="High Humidity Alert",
            icon="💧",
            description="Risk of fungal diseases. Monitor crops closely."
        ))

    # Crop-specific recommendations
    crop_type = additional_params.get("crop_type")
    if crop_type == "tomato":
        if 20 <= temp <= 26 and 40 <= humidity <= 70:
            recommendations.append(Recommendation(
                item="Ideal Tomato Conditions",
                icon="🍅",
                description="Perfect weather for tomato growth"
            ))
    elif crop_type == "rice":
        if temp > 20 and precipitation > 100:
            recommendations.append(Recommendation(
                item="Good Rice Growing Conditions",
                icon="🌾",
                description="Warm and wet conditions favor rice cultivation"
            ))

    return recommendations
