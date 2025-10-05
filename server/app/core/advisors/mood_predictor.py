"""
Climate Mood Predictor

Provides wellness and mood recommendations based on weather conditions.
Analyzes how weather affects mood and suggests appropriate activities.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import math


class MoodPredictor:
    """Climate-based mood and wellness predictor."""
    
    # Weather-mood correlation factors
    MOOD_FACTORS = {
        "temperature": {
            "optimal_range": (20, 25),  # Celsius
            "comfort_zone": (18, 28),
            "mood_impact": "high"
        },
        "sunlight": {
            "optimal_range": (5, 8),  # kWh/m²/day
            "mood_impact": "very_high"
        },
        "precipitation": {
            "optimal_range": (0, 5),  # mm/day
            "mood_impact": "medium"
        },
        "humidity": {
            "optimal_range": (40, 70),  # %
            "mood_impact": "medium"
        }
    }
    
    # Activity recommendations based on weather
    ACTIVITY_RECOMMENDATIONS = {
        "sunny_warm": {
            "mood": "energetic",
            "activities": [
                "Outdoor exercise (running, cycling, hiking)",
                "Beach or pool activities",
                "Gardening or outdoor hobbies",
                "Social gatherings outdoors",
                "Photography or nature walks"
            ],
            "wellness_tips": [
                "Apply sunscreen (SPF 30+)",
                "Stay hydrated",
                "Wear light, breathable clothing",
                "Take breaks in shade"
            ]
        },
        "sunny_cool": {
            "mood": "refreshed",
            "activities": [
                "Light outdoor exercise",
                "Coffee or tea outdoors",
                "Reading in a park",
                "Outdoor sports",
                "Walking or jogging"
            ],
            "wellness_tips": [
                "Layer clothing for temperature changes",
                "Enjoy the fresh air",
                "Perfect for outdoor meditation"
            ]
        },
        "cloudy_mild": {
            "mood": "calm",
            "activities": [
                "Indoor creative projects",
                "Cooking or baking",
                "Reading or studying",
                "Light exercise indoors",
                "Social activities at home"
            ],
            "wellness_tips": [
                "Good for focused work",
                "Consider vitamin D supplements",
                "Maintain regular sleep schedule"
            ]
        },
        "rainy": {
            "mood": "cozy",
            "activities": [
                "Indoor relaxation (reading, movies)",
                "Creative indoor projects",
                "Cooking comfort food",
                "Indoor exercise or yoga",
                "Socializing at home"
            ],
            "wellness_tips": [
                "Perfect for self-care day",
                "Listen to calming music",
                "Practice mindfulness or meditation",
                "Stay warm and comfortable"
            ]
        },
        "hot_humid": {
            "mood": "lethargic",
            "activities": [
                "Swimming or water activities",
                "Indoor air-conditioned activities",
                "Light indoor exercise",
                "Cold beverages and light meals",
                "Early morning or evening activities"
            ],
            "wellness_tips": [
                "Stay hydrated with water and electrolytes",
                "Avoid strenuous outdoor activities",
                "Use fans or air conditioning",
                "Wear loose, light clothing"
            ]
        },
        "cold_dry": {
            "mood": "withdrawn",
            "activities": [
                "Indoor warm activities",
                "Hot beverages and comfort food",
                "Indoor exercise or dancing",
                "Social gatherings indoors",
                "Warm baths or sauna"
            ],
            "wellness_tips": [
                "Use humidifier to prevent dry skin",
                "Layer clothing for warmth",
                "Stay active to maintain body heat",
                "Consider light therapy for mood"
            ]
        }
    }
    
    def generate_recommendations(self, parameter_values: Dict[str, float], 
                               additional_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mood and wellness recommendations based on weather parameters.
        
        Args:
            parameter_values: Weather parameters (T2M, ALLSKY_SFC_SW_DWN, PRECTOTCORR, RH2M)
            additional_params: Additional parameters like sensitivity_level, preferences, etc.
            
        Returns:
            Dictionary with mood predictions and wellness recommendations
        """
        sensitivity_level = additional_params.get("sensitivity_level", "normal")
        user_preferences = additional_params.get("preferences", {})
        location = additional_params.get("location", "Unknown")
        
        # Extract weather parameters
        temperature = parameter_values.get("T2M", 22)
        sunlight = parameter_values.get("ALLSKY_SFC_SW_DWN", 5)
        precipitation = parameter_values.get("PRECTOTCORR", 2)
        humidity = parameter_values.get("RH2M", 60)
        
        # Calculate mood score
        mood_score = self._calculate_mood_score(temperature, sunlight, precipitation, humidity)
        
        # Determine weather category
        weather_category = self._categorize_weather(temperature, sunlight, precipitation, humidity)
        
        # Generate recommendations
        recommendations = {
            "location": location,
            "current_weather": {
                "temperature": temperature,
                "sunlight": sunlight,
                "precipitation": precipitation,
                "humidity": humidity
            },
            "mood_prediction": {
                "overall_score": mood_score,
                "predicted_mood": self._predict_mood(mood_score, weather_category),
                "confidence": self._calculate_confidence(temperature, sunlight, precipitation, humidity),
                "factors": self._analyze_mood_factors(temperature, sunlight, precipitation, humidity)
            },
            "wellness_recommendations": self._generate_wellness_recommendations(
                weather_category, mood_score, sensitivity_level, user_preferences
            ),
            "activity_suggestions": self._suggest_activities(weather_category, mood_score),
            "health_considerations": self._assess_health_considerations(
                temperature, sunlight, precipitation, humidity, sensitivity_level
            ),
            "daily_tips": self._generate_daily_tips(weather_category, mood_score)
        }
        
        return recommendations
    
    def _calculate_mood_score(self, temperature: float, sunlight: float, 
                            precipitation: float, humidity: float) -> float:
        """Calculate overall mood score (0-100) based on weather factors."""
        
        # Temperature score (0-100)
        temp_score = self._score_temperature(temperature)
        
        # Sunlight score (0-100)
        sun_score = self._score_sunlight(sunlight)
        
        # Precipitation score (0-100)
        precip_score = self._score_precipitation(precipitation)
        
        # Humidity score (0-100)
        humidity_score = self._score_humidity(humidity)
        
        # Weighted average (sunlight has highest impact on mood)
        weights = {"temperature": 0.3, "sunlight": 0.4, "precipitation": 0.2, "humidity": 0.1}
        
        mood_score = (
            temp_score * weights["temperature"] +
            sun_score * weights["sunlight"] +
            precip_score * weights["precipitation"] +
            humidity_score * weights["humidity"]
        )
        
        return round(mood_score, 1)
    
    def _score_temperature(self, temperature: float) -> float:
        """Score temperature for mood impact (0-100)."""
        optimal_min, optimal_max = self.MOOD_FACTORS["temperature"]["optimal_range"]
        comfort_min, comfort_max = self.MOOD_FACTORS["temperature"]["comfort_zone"]
        
        if optimal_min <= temperature <= optimal_max:
            return 100.0
        elif comfort_min <= temperature <= comfort_max:
            # Linear interpolation within comfort zone
            if temperature < optimal_min:
                return 80 + (temperature - comfort_min) / (optimal_min - comfort_min) * 20
            else:
                return 80 + (comfort_max - temperature) / (comfort_max - optimal_max) * 20
        else:
            # Outside comfort zone
            if temperature < comfort_min:
                return max(0, 80 - (comfort_min - temperature) * 10)
            else:
                return max(0, 80 - (temperature - comfort_max) * 10)
    
    def _score_sunlight(self, sunlight: float) -> float:
        """Score sunlight for mood impact (0-100)."""
        optimal_min, optimal_max = self.MOOD_FACTORS["sunlight"]["optimal_range"]
        
        if optimal_min <= sunlight <= optimal_max:
            return 100.0
        elif sunlight < optimal_min:
            return max(0, sunlight / optimal_min * 100)
        else:
            # Too much sunlight can be overwhelming
            return max(0, 100 - (sunlight - optimal_max) * 5)
    
    def _score_precipitation(self, precipitation: float) -> float:
        """Score precipitation for mood impact (0-100)."""
        optimal_min, optimal_max = self.MOOD_FACTORS["precipitation"]["optimal_range"]
        
        if optimal_min <= precipitation <= optimal_max:
            return 100.0
        elif precipitation < optimal_min:
            return 100.0  # No rain is generally good for mood
        else:
            # Heavy rain can negatively impact mood
            return max(0, 100 - (precipitation - optimal_max) * 10)
    
    def _score_humidity(self, humidity: float) -> float:
        """Score humidity for mood impact (0-100)."""
        optimal_min, optimal_max = self.MOOD_FACTORS["humidity"]["optimal_range"]
        
        if optimal_min <= humidity <= optimal_max:
            return 100.0
        elif humidity < optimal_min:
            return max(0, 100 - (optimal_min - humidity) * 2)
        else:
            return max(0, 100 - (humidity - optimal_max) * 2)
    
    def _categorize_weather(self, temperature: float, sunlight: float, 
                          precipitation: float, humidity: float) -> str:
        """Categorize weather into mood-relevant categories."""
        
        if precipitation > 10:  # Heavy rain
            return "rainy"
        elif sunlight > 6 and temperature > 28:
            return "sunny_warm"
        elif sunlight > 4 and 15 <= temperature <= 25:
            return "sunny_cool"
        elif temperature > 30 and humidity > 70:
            return "hot_humid"
        elif temperature < 10 and humidity < 40:
            return "cold_dry"
        else:
            return "cloudy_mild"
    
    def _predict_mood(self, mood_score: float, weather_category: str) -> str:
        """Predict mood based on score and weather category."""
        
        if mood_score >= 80:
            return "excellent"
        elif mood_score >= 65:
            return "good"
        elif mood_score >= 50:
            return "neutral"
        elif mood_score >= 35:
            return "low"
        else:
            return "poor"
    
    def _calculate_confidence(self, temperature: float, sunlight: float, 
                            precipitation: float, humidity: float) -> float:
        """Calculate confidence in mood prediction (0-1)."""
        
        # Higher confidence when weather is more extreme or clearly defined
        temp_confidence = min(1.0, abs(temperature - 22) / 10)  # More extreme = higher confidence
        sun_confidence = min(1.0, abs(sunlight - 5) / 3)
        precip_confidence = min(1.0, precipitation / 10)
        
        # Average confidence
        confidence = (temp_confidence + sun_confidence + precip_confidence) / 3
        return round(confidence, 2)
    
    def _analyze_mood_factors(self, temperature: float, sunlight: float, 
                            precipitation: float, humidity: float) -> List[Dict[str, Any]]:
        """Analyze individual factors affecting mood."""
        
        factors = []
        
        # Temperature factor
        temp_score = self._score_temperature(temperature)
        factors.append({
            "factor": "temperature",
            "value": temperature,
            "score": temp_score,
            "impact": "positive" if temp_score > 70 else "negative" if temp_score < 40 else "neutral",
            "description": self._get_temperature_description(temperature)
        })
        
        # Sunlight factor
        sun_score = self._score_sunlight(sunlight)
        factors.append({
            "factor": "sunlight",
            "value": sunlight,
            "score": sun_score,
            "impact": "positive" if sun_score > 70 else "negative" if sun_score < 40 else "neutral",
            "description": self._get_sunlight_description(sunlight)
        })
        
        # Precipitation factor
        precip_score = self._score_precipitation(precipitation)
        factors.append({
            "factor": "precipitation",
            "value": precipitation,
            "score": precip_score,
            "impact": "positive" if precip_score > 70 else "negative" if precip_score < 40 else "neutral",
            "description": self._get_precipitation_description(precipitation)
        })
        
        # Humidity factor
        humidity_score = self._score_humidity(humidity)
        factors.append({
            "factor": "humidity",
            "value": humidity,
            "score": humidity_score,
            "impact": "positive" if humidity_score > 70 else "negative" if humidity_score < 40 else "neutral",
            "description": self._get_humidity_description(humidity)
        })
        
        return factors
    
    def _generate_wellness_recommendations(self, weather_category: str, mood_score: float,
                                         sensitivity_level: str, user_preferences: Dict) -> Dict[str, Any]:
        """Generate wellness recommendations based on weather and mood."""
        
        base_recommendations = self.ACTIVITY_RECOMMENDATIONS.get(weather_category, {
            "mood": "neutral",
            "activities": ["General indoor activities"],
            "wellness_tips": ["Maintain regular routine"]
        })
        
        # Adjust based on mood score
        if mood_score < 40:
            # Low mood - focus on comfort and self-care
            base_recommendations["wellness_tips"].extend([
                "Consider light therapy if available",
                "Engage in gentle physical activity",
                "Connect with friends or family",
                "Practice gratitude or mindfulness"
            ])
        elif mood_score > 80:
            # High mood - capitalize on energy
            base_recommendations["wellness_tips"].extend([
                "Take advantage of high energy",
                "Plan outdoor activities",
                "Try new experiences",
                "Share positive energy with others"
            ])
        
        # Adjust for sensitivity level
        if sensitivity_level == "high":
            base_recommendations["wellness_tips"].extend([
                "Take breaks from weather exposure",
                "Monitor mood changes closely",
                "Have backup indoor plans ready"
            ])
        
        return {
            "mood_category": base_recommendations["mood"],
            "activities": base_recommendations["activities"],
            "wellness_tips": base_recommendations["wellness_tips"],
            "energy_level": self._assess_energy_level(mood_score, weather_category),
            "social_recommendations": self._get_social_recommendations(mood_score, weather_category)
        }
    
    def _suggest_activities(self, weather_category: str, mood_score: float) -> List[Dict[str, Any]]:
        """Suggest specific activities based on weather and mood."""
        
        base_activities = self.ACTIVITY_RECOMMENDATIONS.get(weather_category, {
            "activities": ["General indoor activities"]
        })["activities"]
        
        activities = []
        for activity in base_activities:
            activities.append({
                "name": activity,
                "suitability": self._rate_activity_suitability(activity, mood_score),
                "duration": self._suggest_duration(activity, mood_score),
                "preparation": self._get_activity_preparation(activity, weather_category)
            })
        
        return activities
    
    def _assess_health_considerations(self, temperature: float, sunlight: float,
                                    precipitation: float, humidity: float, 
                                    sensitivity_level: str) -> List[Dict[str, Any]]:
        """Assess health considerations based on weather conditions."""
        
        considerations = []
        
        # Temperature considerations
        if temperature > 30:
            considerations.append({
                "type": "heat_health",
                "level": "warning",
                "message": "High temperature - risk of heat exhaustion",
                "recommendations": [
                    "Stay hydrated",
                    "Avoid prolonged sun exposure",
                    "Wear light clothing",
                    "Take frequent breaks"
                ]
            })
        elif temperature < 5:
            considerations.append({
                "type": "cold_health",
                "level": "warning",
                "message": "Low temperature - risk of hypothermia",
                "recommendations": [
                    "Dress in layers",
                    "Limit outdoor time",
                    "Stay dry",
                    "Keep extremities warm"
                ]
            })
        
        # Sunlight considerations
        if sunlight > 6:
            considerations.append({
                "type": "uv_protection",
                "level": "info",
                "message": "High UV exposure - protect skin and eyes",
                "recommendations": [
                    "Use sunscreen (SPF 30+)",
                    "Wear sunglasses",
                    "Seek shade during peak hours",
                    "Wear protective clothing"
                ]
            })
        elif sunlight < 2:
            considerations.append({
                "type": "vitamin_d",
                "level": "info",
                "message": "Low sunlight - consider vitamin D",
                "recommendations": [
                    "Consider vitamin D supplements",
                    "Eat vitamin D rich foods",
                    "Use light therapy if available",
                    "Spend time near windows"
                ]
            })
        
        # Humidity considerations
        if humidity > 80:
            considerations.append({
                "type": "humidity_health",
                "level": "info",
                "message": "High humidity - increased fungal risk",
                "recommendations": [
                    "Keep skin dry",
                    "Use antifungal powder if needed",
                    "Wear breathable fabrics",
                    "Maintain good hygiene"
                ]
            })
        elif humidity < 30:
            considerations.append({
                "type": "dry_air",
                "level": "info",
                "message": "Low humidity - dry skin and respiratory issues",
                "recommendations": [
                    "Use humidifier",
                    "Apply moisturizer",
                    "Stay hydrated",
                    "Use nasal saline spray"
                ]
            })
        
        return considerations
    
    def _generate_daily_tips(self, weather_category: str, mood_score: float) -> List[str]:
        """Generate daily wellness tips based on weather and mood."""
        
        tips = []
        
        # Weather-specific tips
        if weather_category == "rainy":
            tips.extend([
                "Perfect day for indoor self-care",
                "Try a new recipe or read a book",
                "Practice mindfulness or meditation",
                "Call a friend or family member"
            ])
        elif weather_category == "sunny_warm":
            tips.extend([
                "Great day for outdoor activities",
                "Don't forget sunscreen and hydration",
                "Consider early morning or evening activities",
                "Take advantage of natural vitamin D"
            ])
        elif weather_category == "hot_humid":
            tips.extend([
                "Stay cool and hydrated",
                "Plan indoor activities for peak heat",
                "Use fans or air conditioning",
                "Wear light, breathable clothing"
            ])
        
        # Mood-based tips
        if mood_score < 50:
            tips.extend([
                "Be gentle with yourself today",
                "Focus on small, achievable tasks",
                "Consider talking to someone you trust",
                "Remember that weather affects everyone's mood"
            ])
        elif mood_score > 80:
            tips.extend([
                "Take advantage of your positive energy",
                "Try something new or challenging",
                "Share your good mood with others",
                "Plan activities you've been putting off"
            ])
        
        return tips[:5]  # Return top 5 tips
    
    # Helper methods
    def _get_temperature_description(self, temperature: float) -> str:
        """Get human-readable temperature description."""
        if temperature < 0:
            return "Freezing cold"
        elif temperature < 10:
            return "Very cold"
        elif temperature < 20:
            return "Cool"
        elif temperature < 25:
            return "Pleasant"
        elif temperature < 30:
            return "Warm"
        elif temperature < 35:
            return "Hot"
        else:
            return "Very hot"
    
    def _get_sunlight_description(self, sunlight: float) -> str:
        """Get human-readable sunlight description."""
        if sunlight < 1:
            return "Very cloudy/dark"
        elif sunlight < 3:
            return "Cloudy"
        elif sunlight < 5:
            return "Partly cloudy"
        elif sunlight < 7:
            return "Sunny"
        else:
            return "Very sunny/bright"
    
    def _get_precipitation_description(self, precipitation: float) -> str:
        """Get human-readable precipitation description."""
        if precipitation < 1:
            return "Dry"
        elif precipitation < 5:
            return "Light rain"
        elif precipitation < 15:
            return "Moderate rain"
        else:
            return "Heavy rain"
    
    def _get_humidity_description(self, humidity: float) -> str:
        """Get human-readable humidity description."""
        if humidity < 30:
            return "Very dry"
        elif humidity < 50:
            return "Dry"
        elif humidity < 70:
            return "Comfortable"
        elif humidity < 80:
            return "Humid"
        else:
            return "Very humid"
    
    def _assess_energy_level(self, mood_score: float, weather_category: str) -> str:
        """Assess expected energy level."""
        if mood_score > 75 and weather_category in ["sunny_warm", "sunny_cool"]:
            return "high"
        elif mood_score < 40 or weather_category in ["rainy", "hot_humid"]:
            return "low"
        else:
            return "moderate"
    
    def _get_social_recommendations(self, mood_score: float, weather_category: str) -> List[str]:
        """Get social activity recommendations."""
        if mood_score > 70 and weather_category in ["sunny_warm", "sunny_cool"]:
            return [
                "Great day for social gatherings",
                "Consider outdoor group activities",
                "Perfect for meeting new people"
            ]
        elif mood_score < 50 or weather_category == "rainy":
            return [
                "Small, intimate gatherings work best",
                "Consider one-on-one conversations",
                "Virtual socializing might be more comfortable"
            ]
        else:
            return [
                "Mixed indoor/outdoor social activities",
                "Group size depends on your comfort level"
            ]
    
    def _rate_activity_suitability(self, activity: str, mood_score: float) -> str:
        """Rate how suitable an activity is for current mood."""
        if "outdoor" in activity.lower() and mood_score < 40:
            return "low"
        elif "exercise" in activity.lower() and mood_score > 70:
            return "high"
        elif "relaxation" in activity.lower() and mood_score < 50:
            return "high"
        else:
            return "moderate"
    
    def _suggest_duration(self, activity: str, mood_score: float) -> str:
        """Suggest activity duration based on mood."""
        if mood_score < 40:
            return "15-30 minutes"
        elif mood_score > 80:
            return "1-2 hours"
        else:
            return "30-60 minutes"
    
    def _get_activity_preparation(self, activity: str, weather_category: str) -> List[str]:
        """Get preparation tips for activities."""
        prep = []
        
        if "outdoor" in activity.lower():
            if weather_category == "sunny_warm":
                prep.extend(["Sunscreen", "Hat", "Water bottle"])
            elif weather_category == "rainy":
                prep.extend(["Rain jacket", "Umbrella", "Waterproof shoes"])
            elif weather_category == "hot_humid":
                prep.extend(["Extra water", "Light clothing", "Cooling towel"])
        
        if "exercise" in activity.lower():
            prep.extend(["Comfortable shoes", "Appropriate clothing", "Water bottle"])
        
        return prep


# Create a global instance for easy import
mood_predictor = MoodPredictor()


def generate_recommendations(parameter_values: Dict[str, float], 
                           additional_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate climate mood predictions and wellness suggestions.
    
    Args:
        parameter_values: A dictionary of weather parameters (e.g., T2M, ALLSKY_SFC_SW_DWN).
        additional_params: Advisor-specific parameters (e.g., moodSensitivity).
        
    Returns:
        A dictionary containing mood score, wellness recommendations, and activity suggestions.
    """
    return mood_predictor.generate_recommendations(parameter_values, additional_params)