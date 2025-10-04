from typing import Dict, List
from app.models.responses import Recommendation


def generate_recommendations(
    parameters: Dict[str, float],
    additional_params: Dict
) -> List[Recommendation]:
    """
    Generate wellness recommendations based on weather mood.

    Args:
        parameters: Dictionary of weather parameter values
        additional_params: Additional user preferences

    Returns:
        List of wellness recommendations
    """
    recommendations = []

    temp = parameters.get("T2M", 20)
    sunshine = parameters.get("ALLSKY_SFC_SW_DWN", 0)
    precipitation = parameters.get("PRECTOTCORR", 0)
    humidity = parameters.get("RH2M", 50)

    # Determine weather mood
    if sunshine > 6 and temp > 20 and precipitation < 1:
        mood = "Energetic & Bright"
        recommendations.append(Recommendation(
            item="Outdoor Exercise",
            icon="🏃",
            description="Perfect day for outdoor activities and exercise"
        ))
        recommendations.append(Recommendation(
            item="Vitamin D Boost",
            icon="☀️",
            description="Great sunlight for natural vitamin D"
        ))
    elif precipitation > 10:
        mood = "Cozy & Reflective"
        recommendations.append(Recommendation(
            item="Indoor Activities",
            icon="📚",
            description="Ideal for reading, creative work, or meditation"
        ))
        recommendations.append(Recommendation(
            item="Warm Beverages",
            icon="☕",
            description="Perfect weather for hot tea or coffee"
        ))
    elif temp < 10:
        mood = "Crisp & Invigorating"
        recommendations.append(Recommendation(
            item="Brisk Walk",
            icon="🚶",
            description="Cool weather perfect for energizing walks"
        ))
        recommendations.append(Recommendation(
            item="Warm Layers",
            icon="🧣",
            description="Bundle up and enjoy the fresh air"
        ))
    elif sunshine < 3:
        mood = "Calm & Mellow"
        recommendations.append(Recommendation(
            item="Self-Care Time",
            icon="🧘",
            description="Overcast days are great for introspection"
        ))
        recommendations.append(Recommendation(
            item="Light Therapy",
            icon="💡",
            description="Consider bright indoor lighting"
        ))
    else:
        mood = "Balanced & Pleasant"
        recommendations.append(Recommendation(
            item="Balanced Activities",
            icon="⚖️",
            description="Mix of indoor and outdoor activities"
        ))

    # Add mood as first recommendation
    recommendations.insert(0, Recommendation(
        item=f"Weather Mood: {mood}",
        icon="🌈",
        description="Overall atmospheric feeling"
    ))

    # Humidity-based wellness tips
    if humidity > 80:
        recommendations.append(Recommendation(
            item="Stay Hydrated",
            icon="💧",
            description="High humidity can be draining"
        ))
    elif humidity < 30:
        recommendations.append(Recommendation(
            item="Moisturize",
            icon="🧴",
            description="Low humidity may dry out skin"
        ))

    return recommendations
