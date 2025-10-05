"""
Crop & Farming Advisor

Provides agricultural recommendations based on weather conditions for different crops.
Supports common crops like tomatoes, rice, wheat, corn, and potatoes.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import math


class CropAdvisor:
    """Agricultural advisor for crop-specific recommendations."""
    
    # Crop-specific optimal conditions
    CROP_REQUIREMENTS = {
        "tomato": {
            "optimal_temp_range": (18, 25),
            "min_temp": 10,
            "max_temp": 35,
            "optimal_precipitation": (25, 50),  # mm/month
            "min_precipitation": 10,
            "max_precipitation": 100,
            "growing_season_months": [3, 4, 5, 6, 7, 8, 9, 10],  # March-October
            "frost_sensitive": True,
            "drought_tolerance": "medium"
        },
        "rice": {
            "optimal_temp_range": (20, 30),
            "min_temp": 15,
            "max_temp": 35,
            "optimal_precipitation": (100, 200),  # mm/month
            "min_precipitation": 50,
            "max_precipitation": 300,
            "growing_season_months": [6, 7, 8, 9, 10, 11],  # June-November
            "frost_sensitive": True,
            "drought_tolerance": "low"
        },
        "wheat": {
            "optimal_temp_range": (15, 25),
            "min_temp": 5,
            "max_temp": 30,
            "optimal_precipitation": (30, 60),  # mm/month
            "min_precipitation": 20,
            "max_precipitation": 100,
            "growing_season_months": [10, 11, 12, 1, 2, 3, 4],  # October-April
            "frost_sensitive": False,
            "drought_tolerance": "high"
        },
        "corn": {
            "optimal_temp_range": (20, 30),
            "min_temp": 10,
            "max_temp": 35,
            "optimal_precipitation": (50, 100),  # mm/month
            "min_precipitation": 30,
            "max_precipitation": 150,
            "growing_season_months": [4, 5, 6, 7, 8, 9],  # April-September
            "frost_sensitive": True,
            "drought_tolerance": "medium"
        },
        "potato": {
            "optimal_temp_range": (15, 20),
            "min_temp": 5,
            "max_temp": 25,
            "optimal_precipitation": (40, 80),  # mm/month
            "min_precipitation": 20,
            "max_precipitation": 120,
            "growing_season_months": [10, 11, 12, 1, 2, 3, 4],  # October-April
            "frost_sensitive": True,
            "drought_tolerance": "medium"
        }
    }
    
    def generate_recommendations(self, parameter_values: Dict[str, float], 
                               additional_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate crop farming recommendations based on weather parameters.

    Args:
            parameter_values: Weather parameters (T2M, PRECTOTCORR, T2M_MIN, T2M_MAX, RH2M)
            additional_params: Additional parameters like crop_type, planting_date, etc.

    Returns:
            Dictionary with farming recommendations
        """
        crop_type = additional_params.get("crop_type", "tomato").lower()
        planting_date = additional_params.get("planting_date")
        location = additional_params.get("location", "Unknown")
        
        if crop_type not in self.CROP_REQUIREMENTS:
            return {
                "error": f"Unsupported crop type: {crop_type}",
                "supported_crops": list(self.CROP_REQUIREMENTS.keys())
            }
        
        crop_req = self.CROP_REQUIREMENTS[crop_type]
        
        # Extract weather parameters
        temp = parameter_values.get("T2M", 20)
        temp_min = parameter_values.get("T2M_MIN", temp - 5)
        temp_max = parameter_values.get("T2M_MAX", temp + 5)
        precipitation = parameter_values.get("PRECTOTCORR", 50)
        humidity = parameter_values.get("RH2M", 60)
        
        # Calculate current month (assuming this is for current conditions)
        current_month = datetime.now().month
        
        # Generate recommendations
        recommendations = {
            "crop_type": crop_type,
            "location": location,
            "current_conditions": self._analyze_current_conditions(
                temp, temp_min, temp_max, precipitation, humidity, crop_req
            ),
            "planting_window": self._calculate_planting_window(crop_req, current_month),
            "risk_assessment": self._assess_risks(temp, temp_min, temp_max, precipitation, crop_req),
            "alerts": self._generate_alerts(temp, temp_min, temp_max, precipitation, crop_req),
            "expected_conditions": self._predict_conditions(temp, precipitation, crop_req),
            "recommendations": self._generate_actionable_recommendations(
                temp, precipitation, humidity, crop_req, current_month
            )
        }
        
        return recommendations
    
    def _analyze_current_conditions(self, temp: float, temp_min: float, temp_max: float,
                                  precipitation: float, humidity: float, 
                                  crop_req: Dict) -> Dict[str, Any]:
        """Analyze current weather conditions for the crop."""
        
        # Temperature analysis
        temp_score = self._score_temperature(temp, crop_req)
        temp_risk = self._assess_temperature_risk(temp, temp_min, temp_max, crop_req)
        
        # Precipitation analysis
        precip_score = self._score_precipitation(precipitation, crop_req)
        precip_risk = self._assess_precipitation_risk(precipitation, crop_req)
        
        # Overall condition score
        overall_score = (temp_score + precip_score) / 2
        
        return {
            "temperature": {
                "current": temp,
                "min": temp_min,
                "max": temp_max,
                "score": temp_score,
                "risk_level": temp_risk["level"],
                "assessment": temp_risk["message"]
            },
            "precipitation": {
                "current": precipitation,
                "score": precip_score,
                "risk_level": precip_risk["level"],
                "assessment": precip_risk["message"]
            },
            "humidity": {
                "current": humidity,
                "assessment": self._assess_humidity(humidity, crop_req)
            },
            "overall_score": overall_score,
            "condition_summary": self._get_condition_summary(overall_score)
        }
    
    def _calculate_planting_window(self, crop_req: Dict, current_month: int) -> Dict[str, Any]:
        """Calculate optimal planting window for the crop."""
        
        growing_months = crop_req["growing_season_months"]
        
        # Find next planting window
        next_planting_months = [m for m in growing_months if m >= current_month]
        if not next_planting_months:
            # If no months left this year, use first month of next year
            next_planting_months = [growing_months[0]]
        
        # Calculate planting dates (approximate)
        planting_start = next_planting_months[0]
        planting_end = min(planting_start + 2, max(growing_months))  # 2-month window
        
        return {
            "optimal_months": next_planting_months[:3],  # Next 3 optimal months
            "planting_window": f"Month {planting_start} to {planting_end}",
            "confidence": 0.85,
            "notes": self._get_planting_notes(crop_req, current_month)
        }
    
    def _assess_risks(self, temp: float, temp_min: float, temp_max: float,
                     precipitation: float, crop_req: Dict) -> Dict[str, Any]:
        """Assess various risks for the crop."""
        
        risks = []
        
        # Frost risk
        if crop_req["frost_sensitive"] and temp_min < 5:
            risks.append({
                "type": "frost",
                "level": "high" if temp_min < 0 else "medium",
                "probability": self._calculate_frost_probability(temp_min),
                "message": f"Frost risk detected. Minimum temperature: {temp_min:.1f}°C"
            })
        
        # Heat stress risk
        if temp_max > crop_req["max_temp"]:
            risks.append({
                "type": "heat_stress",
                "level": "high",
                "probability": 0.9,
                "message": f"High temperature risk. Maximum temperature: {temp_max:.1f}°C"
            })
        
        # Drought risk
        if precipitation < crop_req["min_precipitation"]:
            risks.append({
                "type": "drought",
                "level": "high" if precipitation < crop_req["min_precipitation"] * 0.5 else "medium",
                "probability": self._calculate_drought_probability(precipitation, crop_req),
                "message": f"Low precipitation: {precipitation:.1f}mm. Irrigation recommended."
            })
        
        # Excessive rain risk
        if precipitation > crop_req["max_precipitation"]:
            risks.append({
                "type": "excessive_rain",
                "level": "high",
                "probability": 0.8,
                "message": f"Excessive precipitation: {precipitation:.1f}mm. Drainage needed."
            })
        
        # Overall risk level
        if not risks:
            overall_risk = "low"
        elif any(r["level"] == "high" for r in risks):
            overall_risk = "high"
        else:
            overall_risk = "medium"
        
        return {
            "overall": overall_risk,
            "factors": risks,
            "risk_summary": self._get_risk_summary(overall_risk, len(risks))
        }
    
    def _generate_alerts(self, temp: float, temp_min: float, temp_max: float,
                        precipitation: float, crop_req: Dict) -> List[Dict[str, Any]]:
        """Generate immediate alerts for the farmer."""
        
        alerts = []
        
        # Critical temperature alerts
        if temp_min < 0:
            alerts.append({
                "type": "critical",
                "message": "FROST WARNING: Freezing temperatures detected. Protect crops immediately.",
                "action": "Cover crops with frost cloth or move to greenhouse",
                "urgency": "immediate"
            })
        elif temp_max > crop_req["max_temp"] + 5:
            alerts.append({
                "type": "warning",
                "message": f"HEAT STRESS: Temperature {temp_max:.1f}°C exceeds crop tolerance.",
                "action": "Increase irrigation and provide shade",
                "urgency": "high"
            })
        
        # Precipitation alerts
        if precipitation < crop_req["min_precipitation"] * 0.3:
            alerts.append({
                "type": "warning",
                "message": "DROUGHT ALERT: Very low precipitation. Irrigation required.",
                "action": "Implement irrigation system or water manually",
                "urgency": "high"
            })
        elif precipitation > crop_req["max_precipitation"] * 1.5:
            alerts.append({
                "type": "warning",
                "message": "FLOOD RISK: Excessive rainfall. Check drainage.",
                "action": "Ensure proper drainage and consider raised beds",
                "urgency": "medium"
            })
        
        return alerts
    
    def _predict_conditions(self, temp: float, precipitation: float, 
                          crop_req: Dict) -> Dict[str, Any]:
        """Predict expected conditions for the next few months."""
        
        # Simple prediction based on current conditions (in real implementation,
        # this would use historical data and weather forecasts)
        temp_trend = "stable"  # Would be calculated from historical data
        precip_trend = "stable"
        
        return {
            "next_30_days": {
                "avg_temperature": temp,
                "total_precipitation": precipitation * 1.1,  # Slight increase
                "confidence": 0.7
            },
            "next_90_days": {
                "avg_temperature": temp,
                "total_precipitation": precipitation * 3.2,  # Seasonal projection
                "confidence": 0.6
            },
            "trends": {
                "temperature": temp_trend,
                "precipitation": precip_trend
            }
        }
    
    def _generate_actionable_recommendations(self, temp: float, precipitation: float,
                                           humidity: float, crop_req: Dict, 
                                           current_month: int) -> List[Dict[str, Any]]:
        """Generate specific, actionable recommendations for the farmer."""
        
        recommendations = []
        
        # Planting recommendations
        if current_month in crop_req["growing_season_months"]:
            recommendations.append({
                "category": "planting",
                "priority": "high",
                "title": "Optimal Planting Time",
                "description": f"Current month ({current_month}) is ideal for planting {crop_req.get('name', 'this crop')}",
                "action": "Prepare soil and plant seeds/seedlings",
                "timeline": "Within 1-2 weeks"
            })
        
        # Temperature-based recommendations
        if temp < crop_req["optimal_temp_range"][0]:
            recommendations.append({
                "category": "temperature",
                "priority": "medium",
                "title": "Temperature Management",
                "description": f"Temperature {temp:.1f}°C is below optimal range",
                "action": "Consider using row covers or greenhouse",
                "timeline": "Immediate"
            })
        elif temp > crop_req["optimal_temp_range"][1]:
            recommendations.append({
                "category": "temperature",
                "priority": "high",
                "title": "Heat Management",
                "description": f"Temperature {temp:.1f}°C exceeds optimal range",
                "action": "Increase irrigation frequency and provide shade",
                "timeline": "Immediate"
            })
        
        # Water management recommendations
        if precipitation < crop_req["min_precipitation"]:
            recommendations.append({
                "category": "irrigation",
                "priority": "high",
                "title": "Irrigation Required",
                "description": f"Precipitation {precipitation:.1f}mm is insufficient",
                "action": f"Water {crop_req['min_precipitation'] - precipitation:.1f}mm more per month",
                "timeline": "Weekly"
            })
        elif precipitation > crop_req["max_precipitation"]:
            recommendations.append({
                "category": "drainage",
                "priority": "medium",
                "title": "Drainage Management",
                "description": f"Excessive precipitation {precipitation:.1f}mm",
                "action": "Improve drainage and avoid waterlogging",
                "timeline": "Immediate"
            })
        
        return recommendations

    # Helper methods
    def _score_temperature(self, temp: float, crop_req: Dict) -> float:
        """Score temperature on a 0-100 scale."""
        optimal_min, optimal_max = crop_req["optimal_temp_range"]
        
        if optimal_min <= temp <= optimal_max:
            return 100.0
        elif temp < optimal_min:
            return max(0, 100 - (optimal_min - temp) * 10)
        else:
            return max(0, 100 - (temp - optimal_max) * 10)
    
    def _score_precipitation(self, precipitation: float, crop_req: Dict) -> float:
        """Score precipitation on a 0-100 scale."""
        optimal_min, optimal_max = crop_req["optimal_precipitation"]
        
        if optimal_min <= precipitation <= optimal_max:
            return 100.0
        elif precipitation < optimal_min:
            return max(0, 100 - (optimal_min - precipitation) * 2)
        else:
            return max(0, 100 - (precipitation - optimal_max) * 2)
    
    def _assess_temperature_risk(self, temp: float, temp_min: float, temp_max: float, 
                               crop_req: Dict) -> Dict[str, Any]:
        """Assess temperature-related risks."""
        if temp_min < 0 and crop_req["frost_sensitive"]:
            return {"level": "high", "message": "Frost risk - protect crops"}
        elif temp_max > crop_req["max_temp"]:
            return {"level": "high", "message": "Heat stress risk"}
        elif temp < crop_req["optimal_temp_range"][0]:
            return {"level": "medium", "message": "Below optimal temperature"}
        elif temp > crop_req["optimal_temp_range"][1]:
            return {"level": "medium", "message": "Above optimal temperature"}
        else:
            return {"level": "low", "message": "Temperature conditions are good"}
    
    def _assess_precipitation_risk(self, precipitation: float, crop_req: Dict) -> Dict[str, Any]:
        """Assess precipitation-related risks."""
        if precipitation < crop_req["min_precipitation"]:
            return {"level": "high", "message": "Drought risk - irrigation needed"}
        elif precipitation > crop_req["max_precipitation"]:
            return {"level": "high", "message": "Excessive rain - drainage needed"}
        elif precipitation < crop_req["optimal_precipitation"][0]:
            return {"level": "medium", "message": "Below optimal precipitation"}
        elif precipitation > crop_req["optimal_precipitation"][1]:
            return {"level": "medium", "message": "Above optimal precipitation"}
        else:
            return {"level": "low", "message": "Precipitation conditions are good"}
    
    def _assess_humidity(self, humidity: float, crop_req: Dict) -> str:
        """Assess humidity conditions."""
        if humidity < 40:
            return "Low humidity - may need misting"
        elif humidity > 80:
            return "High humidity - watch for fungal diseases"
        else:
            return "Humidity levels are good"
    
    def _calculate_frost_probability(self, temp_min: float) -> float:
        """Calculate probability of frost damage."""
        if temp_min < -2:
            return 0.9
        elif temp_min < 0:
            return 0.7
        elif temp_min < 2:
            return 0.3
        else:
            return 0.0
    
    def _calculate_drought_probability(self, precipitation: float, crop_req: Dict) -> float:
        """Calculate probability of drought stress."""
        min_precip = crop_req["min_precipitation"]
        if precipitation < min_precip * 0.3:
            return 0.9
        elif precipitation < min_precip * 0.6:
            return 0.6
        elif precipitation < min_precip:
            return 0.3
        else:
            return 0.0
    
    def _get_condition_summary(self, overall_score: float) -> str:
        """Get a summary of overall conditions."""
        if overall_score >= 80:
            return "Excellent growing conditions"
        elif overall_score >= 60:
            return "Good growing conditions with minor concerns"
        elif overall_score >= 40:
            return "Moderate conditions requiring attention"
        else:
            return "Poor conditions - significant intervention needed"
    
    def _get_planting_notes(self, crop_req: Dict, current_month: int) -> str:
        """Get planting-specific notes."""
        if current_month in crop_req["growing_season_months"]:
            return "Current month is optimal for planting"
        else:
            next_month = min([m for m in crop_req["growing_season_months"] if m > current_month], 
                           default=crop_req["growing_season_months"][0])
            return f"Wait until month {next_month} for optimal planting"
    
    def _get_risk_summary(self, overall_risk: str, risk_count: int) -> str:
        """Get a summary of risk assessment."""
        if overall_risk == "high":
            return f"High risk with {risk_count} critical factors requiring immediate attention"
        elif overall_risk == "medium":
            return f"Medium risk with {risk_count} factors to monitor"
        else:
            return "Low risk - conditions are generally favorable"


# Create a global instance for easy import
crop_advisor = CropAdvisor()


def generate_recommendations(parameter_values: Dict[str, float], 
                           additional_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate crop and farming recommendations based on weather parameters.
    
    Args:
        parameter_values: A dictionary of weather parameters (e.g., T2M, PRECTOTCORR).
        additional_params: Advisor-specific parameters (e.g., cropType, plantingDate).
        
    Returns:
        A dictionary containing planting window, risk assessment, and alerts.
    """
    return crop_advisor.generate_recommendations(parameter_values, additional_params)