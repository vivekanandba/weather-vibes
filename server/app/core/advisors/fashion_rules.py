"""
AI Fashion Stylist

Provides weather-appropriate outfit recommendations based on current conditions.
Considers temperature, sunlight, precipitation, and wind for styling suggestions.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import math


class FashionStylist:
    """AI-powered fashion stylist for weather-appropriate recommendations."""
    
    # Weather-based styling rules
    STYLING_RULES = {
        "temperature": {
            "freezing": {"range": (-10, 0), "style": "winter_layers"},
            "cold": {"range": (0, 10), "style": "warm_layers"},
            "cool": {"range": (10, 18), "style": "light_layers"},
            "mild": {"range": (18, 25), "style": "comfortable"},
            "warm": {"range": (25, 30), "style": "light_summer"},
            "hot": {"range": (30, 40), "style": "minimal_summer"}
        },
        "precipitation": {
            "none": {"range": (0, 1), "style": "dry_weather"},
            "light": {"range": (1, 5), "style": "light_rain"},
            "moderate": {"range": (5, 15), "style": "moderate_rain"},
            "heavy": {"range": (15, 50), "style": "heavy_rain"}
        },
        "sunlight": {
            "low": {"range": (0, 3), "style": "indoor_focus"},
            "moderate": {"range": (3, 6), "style": "mixed_lighting"},
            "high": {"range": (6, 10), "style": "sun_protection"}
        },
        "wind": {
            "calm": {"range": (0, 3), "style": "flowy_fabrics"},
            "breeze": {"range": (3, 7), "style": "secure_items"},
            "windy": {"range": (7, 15), "style": "wind_resistant"}
        }
    }
    
    # Clothing items database
    CLOTHING_ITEMS = {
        "tops": {
            "tank_top": {"temp_range": (25, 40), "occasions": ["casual", "athletic"], "fabrics": ["cotton", "polyester"]},
            "t_shirt": {"temp_range": (15, 30), "occasions": ["casual", "athletic"], "fabrics": ["cotton", "blend"]},
            "long_sleeve": {"temp_range": (10, 25), "occasions": ["casual", "business"], "fabrics": ["cotton", "wool"]},
            "blouse": {"temp_range": (15, 28), "occasions": ["business", "casual"], "fabrics": ["silk", "cotton", "polyester"]},
            "sweater": {"temp_range": (5, 20), "occasions": ["casual", "business"], "fabrics": ["wool", "cashmere", "cotton"]},
            "hoodie": {"temp_range": (10, 22), "occasions": ["casual", "athletic"], "fabrics": ["cotton", "fleece"]},
            "cardigan": {"temp_range": (12, 25), "occasions": ["casual", "business"], "fabrics": ["wool", "cotton", "cashmere"]},
            "blazer": {"temp_range": (15, 25), "occasions": ["business", "formal"], "fabrics": ["wool", "cotton", "polyester"]},
            "jacket": {"temp_range": (0, 20), "occasions": ["casual", "business"], "fabrics": ["denim", "leather", "cotton"]},
            "coat": {"temp_range": (-10, 15), "occasions": ["formal", "casual"], "fabrics": ["wool", "down", "synthetic"]}
        },
        "bottoms": {
            "shorts": {"temp_range": (20, 40), "occasions": ["casual", "athletic"], "fabrics": ["cotton", "denim"]},
            "skirt": {"temp_range": (15, 30), "occasions": ["casual", "business"], "fabrics": ["cotton", "polyester", "wool"]},
            "jeans": {"temp_range": (5, 30), "occasions": ["casual"], "fabrics": ["denim"]},
            "trousers": {"temp_range": (10, 28), "occasions": ["business", "casual"], "fabrics": ["wool", "cotton", "polyester"]},
            "leggings": {"temp_range": (5, 25), "occasions": ["athletic", "casual"], "fabrics": ["spandex", "cotton"]},
            "dress_pants": {"temp_range": (10, 25), "occasions": ["business", "formal"], "fabrics": ["wool", "polyester"]}
        },
        "outerwear": {
            "rain_jacket": {"temp_range": (5, 25), "occasions": ["casual", "athletic"], "fabrics": ["gore_tex", "nylon"]},
            "windbreaker": {"temp_range": (10, 25), "occasions": ["casual", "athletic"], "fabrics": ["nylon", "polyester"]},
            "puffer_jacket": {"temp_range": (-5, 15), "occasions": ["casual", "athletic"], "fabrics": ["down", "synthetic"]},
            "trench_coat": {"temp_range": (5, 20), "occasions": ["business", "formal"], "fabrics": ["cotton", "polyester"]},
            "denim_jacket": {"temp_range": (10, 25), "occasions": ["casual"], "fabrics": ["denim"]}
        },
        "accessories": {
            "sunglasses": {"conditions": ["sunny"], "occasions": ["all"]},
            "umbrella": {"conditions": ["rainy"], "occasions": ["all"]},
            "scarf": {"temp_range": (0, 20), "occasions": ["casual", "business"]},
            "hat": {"conditions": ["sunny", "cold"], "occasions": ["casual", "athletic"]},
            "gloves": {"temp_range": (-10, 10), "occasions": ["casual", "athletic"]},
            "belt": {"occasions": ["business", "casual"]},
            "watch": {"occasions": ["business", "casual", "formal"]},
            "jewelry": {"occasions": ["business", "casual", "formal"]}
        },
        "shoes": {
            "sneakers": {"temp_range": (5, 35), "occasions": ["casual", "athletic"], "conditions": ["dry", "light_rain"]},
            "boots": {"temp_range": (-5, 20), "occasions": ["casual", "business"], "conditions": ["rainy", "cold"]},
            "sandals": {"temp_range": (20, 40), "occasions": ["casual"], "conditions": ["dry", "warm"]},
            "loafers": {"temp_range": (10, 30), "occasions": ["business", "casual"], "conditions": ["dry"]},
            "heels": {"temp_range": (10, 30), "occasions": ["business", "formal"], "conditions": ["dry"]},
            "rain_boots": {"temp_range": (0, 25), "occasions": ["casual"], "conditions": ["rainy"]},
            "flats": {"temp_range": (10, 30), "occasions": ["casual", "business"], "conditions": ["dry"]}
        }
    }
    
    # Style categories
    STYLE_CATEGORIES = {
        "casual": {"description": "Comfortable, everyday wear", "formality": 1},
        "business": {"description": "Professional, office-appropriate", "formality": 3},
        "athletic": {"description": "Active, sporty wear", "formality": 1},
        "formal": {"description": "Dressy, special occasions", "formality": 5},
        "smart_casual": {"description": "Polished casual", "formality": 2}
    }
    
    def generate_recommendations(self, parameter_values: Dict[str, float], 
                               additional_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate fashion recommendations based on weather parameters.
        
        Args:
            parameter_values: Weather parameters (T2M, ALLSKY_SFC_SW_DWN, PRECTOTCORR, WS2M)
            additional_params: Additional parameters like style_preference, occasion, etc.
            
        Returns:
            Dictionary with fashion recommendations
        """
        style_preference = additional_params.get("style_preference", "casual")
        occasion = additional_params.get("occasion", "casual")
        gender = additional_params.get("gender", "unisex")
        location = additional_params.get("location", "Unknown")
        
        # Extract weather parameters
        temperature = parameter_values.get("T2M", 22)
        sunlight = parameter_values.get("ALLSKY_SFC_SW_DWN", 5)
        precipitation = parameter_values.get("PRECTOTCORR", 2)
        wind_speed = parameter_values.get("WS2M", 3)
        
        # Determine weather conditions
        weather_conditions = self._analyze_weather_conditions(temperature, sunlight, precipitation, wind_speed)
        
        # Generate outfit recommendations
        recommendations = {
            "location": location,
            "weather_conditions": weather_conditions,
            "style_preference": style_preference,
            "occasion": occasion,
            "outfit_recommendations": self._generate_outfits(
                temperature, sunlight, precipitation, wind_speed, style_preference, occasion, gender
            ),
            "accessory_recommendations": self._recommend_accessories(
                temperature, sunlight, precipitation, wind_speed, occasion
            ),
            "color_suggestions": self._suggest_colors(weather_conditions, season=self._get_season()),
            "fabric_recommendations": self._recommend_fabrics(temperature, precipitation, wind_speed),
            "comfort_score": self._calculate_comfort_score(temperature, precipitation, wind_speed),
            "style_notes": self._generate_style_notes(weather_conditions, style_preference, occasion)
        }
        
        return recommendations
    
    def _analyze_weather_conditions(self, temperature: float, sunlight: float, 
                                   precipitation: float, wind_speed: float) -> Dict[str, Any]:
        """Analyze current weather conditions for styling."""
        
        return {
            "temperature": {
                "value": temperature,
                "category": self._categorize_temperature(temperature),
                "description": self._get_temperature_description(temperature)
            },
            "sunlight": {
                "value": sunlight,
                "category": self._categorize_sunlight(sunlight),
                "uv_level": self._assess_uv_level(sunlight)
            },
            "precipitation": {
                "value": precipitation,
                "category": self._categorize_precipitation(precipitation),
                "description": self._get_precipitation_description(precipitation)
            },
            "wind": {
                "value": wind_speed,
                "category": self._categorize_wind(wind_speed),
                "description": self._get_wind_description(wind_speed)
            }
        }
    
    def _generate_outfits(self, temperature: float, sunlight: float, precipitation: float,
                         wind_speed: float, style_preference: str, occasion: str, 
                         gender: str) -> List[Dict[str, Any]]:
        """Generate multiple outfit recommendations."""
        
        outfits = []
        
        # Primary outfit (most weather-appropriate)
        primary_outfit = self._create_outfit(
            temperature, sunlight, precipitation, wind_speed, 
            style_preference, occasion, gender, priority="weather"
        )
        outfits.append(primary_outfit)
        
        # Alternative outfit (style-focused)
        if style_preference != "casual":
            style_outfit = self._create_outfit(
                temperature, sunlight, precipitation, wind_speed,
                style_preference, occasion, gender, priority="style"
            )
            outfits.append(style_outfit)
        
        # Layered outfit (for variable conditions)
        if self._needs_layering(temperature, wind_speed):
            layered_outfit = self._create_outfit(
                temperature, sunlight, precipitation, wind_speed,
                style_preference, occasion, gender, priority="layering"
            )
            outfits.append(layered_outfit)
        
        return outfits
    
    def _create_outfit(self, temperature: float, sunlight: float, precipitation: float,
                      wind_speed: float, style_preference: str, occasion: str, 
                      gender: str, priority: str) -> Dict[str, Any]:
        """Create a specific outfit recommendation."""
        
        outfit = {
            "name": f"{style_preference.title()} {occasion.title()} Outfit",
            "priority": priority,
            "items": [],
            "comfort_score": 0,
            "style_score": 0,
            "weather_appropriateness": 0,
            "notes": []
        }
        
        # Select top
        top = self._select_top(temperature, precipitation, wind_speed, style_preference, occasion)
        outfit["items"].append(top)
        
        # Select bottom
        bottom = self._select_bottom(temperature, precipitation, wind_speed, style_preference, occasion)
        outfit["items"].append(bottom)
        
        # Select outerwear if needed
        if self._needs_outerwear(temperature, precipitation, wind_speed):
            outerwear = self._select_outerwear(temperature, precipitation, wind_speed, style_preference, occasion)
            outfit["items"].append(outerwear)
        
        # Select shoes
        shoes = self._select_shoes(temperature, precipitation, wind_speed, style_preference, occasion)
        outfit["items"].append(shoes)
        
        # Calculate scores
        outfit["comfort_score"] = self._calculate_outfit_comfort(outfit["items"], temperature, wind_speed)
        outfit["style_score"] = self._calculate_outfit_style(outfit["items"], style_preference, occasion)
        outfit["weather_appropriateness"] = self._calculate_weather_appropriateness(
            outfit["items"], temperature, precipitation, wind_speed
        )
        
        # Add notes
        outfit["notes"] = self._generate_outfit_notes(outfit["items"], temperature, precipitation, wind_speed)
        
        return outfit
    
    def _select_top(self, temperature: float, precipitation: float, wind_speed: float,
                   style_preference: str, occasion: str) -> Dict[str, Any]:
        """Select appropriate top based on conditions."""
        
        suitable_tops = []
        
        for top_name, top_data in self.CLOTHING_ITEMS["tops"].items():
            if (top_data["temp_range"][0] <= temperature <= top_data["temp_range"][1] and
                occasion in top_data["occasions"]):
                suitable_tops.append((top_name, top_data))
        
        if not suitable_tops:
            # Fallback to most temperature-appropriate
            suitable_tops = [(name, data) for name, data in self.CLOTHING_ITEMS["tops"].items()
                           if data["temp_range"][0] <= temperature <= data["temp_range"][1]]
        
        # Select best match
        selected_top = suitable_tops[0] if suitable_tops else ("t_shirt", self.CLOTHING_ITEMS["tops"]["t_shirt"])
        
        return {
            "type": "top",
            "name": selected_top[0].replace("_", " ").title(),
            "category": "tops",
            "weather_suitability": self._assess_item_weather_suitability(selected_top[1], temperature, precipitation),
            "style_match": self._assess_style_match(selected_top[1], style_preference),
            "fabric": selected_top[1]["fabrics"][0] if selected_top[1]["fabrics"] else "cotton"
        }
    
    def _select_bottom(self, temperature: float, precipitation: float, wind_speed: float,
                      style_preference: str, occasion: str) -> Dict[str, Any]:
        """Select appropriate bottom based on conditions."""
        
        suitable_bottoms = []
        
        for bottom_name, bottom_data in self.CLOTHING_ITEMS["bottoms"].items():
            if (bottom_data["temp_range"][0] <= temperature <= bottom_data["temp_range"][1] and
                occasion in bottom_data["occasions"]):
                suitable_bottoms.append((bottom_name, bottom_data))
        
        if not suitable_bottoms:
            suitable_bottoms = [(name, data) for name, data in self.CLOTHING_ITEMS["bottoms"].items()
                              if data["temp_range"][0] <= temperature <= data["temp_range"][1]]
        
        selected_bottom = suitable_bottoms[0] if suitable_bottoms else ("jeans", self.CLOTHING_ITEMS["bottoms"]["jeans"])
        
        return {
            "type": "bottom",
            "name": selected_bottom[0].replace("_", " ").title(),
            "category": "bottoms",
            "weather_suitability": self._assess_item_weather_suitability(selected_bottom[1], temperature, precipitation),
            "style_match": self._assess_style_match(selected_bottom[1], style_preference),
            "fabric": selected_bottom[1]["fabrics"][0] if selected_bottom[1]["fabrics"] else "cotton"
        }
    
    def _select_outerwear(self, temperature: float, precipitation: float, wind_speed: float,
                         style_preference: str, occasion: str) -> Dict[str, Any]:
        """Select appropriate outerwear based on conditions."""
        
        if precipitation > 5:
            # Rain protection needed
            outerwear_name = "rain_jacket"
        elif temperature < 10:
            # Cold weather protection
            outerwear_name = "puffer_jacket"
        elif wind_speed > 7:
            # Wind protection needed
            outerwear_name = "windbreaker"
        else:
            # Light layer
            outerwear_name = "cardigan"
        
        outerwear_data = self.CLOTHING_ITEMS["outerwear"].get(outerwear_name, 
                                                             self.CLOTHING_ITEMS["outerwear"]["jacket"])
        
        return {
            "type": "outerwear",
            "name": outerwear_name.replace("_", " ").title(),
            "category": "outerwear",
            "weather_suitability": self._assess_item_weather_suitability(outerwear_data, temperature, precipitation),
            "style_match": self._assess_style_match(outerwear_data, style_preference),
            "fabric": outerwear_data["fabrics"][0] if outerwear_data["fabrics"] else "cotton"
        }
    
    def _select_shoes(self, temperature: float, precipitation: float, wind_speed: float,
                     style_preference: str, occasion: str) -> Dict[str, Any]:
        """Select appropriate shoes based on conditions."""
        
        if precipitation > 10:
            shoe_name = "rain_boots"
        elif precipitation > 5:
            shoe_name = "boots"
        elif temperature > 25:
            shoe_name = "sandals"
        elif occasion == "business":
            shoe_name = "loafers"
        else:
            shoe_name = "sneakers"
        
        shoe_data = self.CLOTHING_ITEMS["shoes"].get(shoe_name, self.CLOTHING_ITEMS["shoes"]["sneakers"])
        
        return {
            "type": "shoes",
            "name": shoe_name.replace("_", " ").title(),
            "category": "shoes",
            "weather_suitability": self._assess_item_weather_suitability(shoe_data, temperature, precipitation),
            "style_match": self._assess_style_match(shoe_data, style_preference),
            "fabric": shoe_data.get("fabrics", ["leather"])[0]
        }
    
    def _recommend_accessories(self, temperature: float, sunlight: float, 
                             precipitation: float, wind_speed: float, occasion: str) -> List[Dict[str, Any]]:
        """Recommend accessories based on weather conditions."""
        
        accessories = []
        
        # Sunglasses for bright conditions
        if sunlight > 6:
            accessories.append({
                "name": "Sunglasses",
                "reason": "High UV protection needed",
                "priority": "high",
                "style_notes": "Choose UV400 protection"
            })
        
        # Umbrella for rain
        if precipitation > 5:
            accessories.append({
                "name": "Umbrella",
                "reason": "Rain protection essential",
                "priority": "high",
                "style_notes": "Compact, wind-resistant preferred"
            })
        
        # Hat for sun or cold
        if sunlight > 6 or temperature < 10:
            hat_type = "Sun hat" if sunlight > 6 else "Warm hat"
            accessories.append({
                "name": hat_type,
                "reason": "Sun protection" if sunlight > 6 else "Warmth",
                "priority": "medium",
                "style_notes": "Match your outfit color"
            })
        
        # Scarf for cold weather
        if temperature < 15:
            accessories.append({
                "name": "Scarf",
                "reason": "Neck warmth and style",
                "priority": "medium",
                "style_notes": "Can add color and texture"
            })
        
        # Gloves for very cold weather
        if temperature < 5:
            accessories.append({
                "name": "Gloves",
                "reason": "Hand protection from cold",
                "priority": "high",
                "style_notes": "Choose touchscreen-compatible if needed"
            })
        
        # Watch for business occasions
        if occasion in ["business", "formal"]:
            accessories.append({
                "name": "Watch",
                "reason": "Professional accessory",
                "priority": "low",
                "style_notes": "Classic, understated design"
            })
        
        return accessories
    
    def _suggest_colors(self, weather_conditions: Dict, season: str) -> Dict[str, List[str]]:
        """Suggest appropriate colors based on weather and season."""
        
        color_suggestions = {
            "primary": [],
            "accent": [],
            "avoid": []
        }
        
        # Temperature-based color suggestions
        temp_category = weather_conditions["temperature"]["category"]
        
        if temp_category in ["freezing", "cold"]:
            color_suggestions["primary"].extend(["navy", "black", "charcoal", "burgundy"])
            color_suggestions["accent"].extend(["cream", "camel", "forest_green"])
        elif temp_category in ["cool", "mild"]:
            color_suggestions["primary"].extend(["navy", "gray", "olive", "brown"])
            color_suggestions["accent"].extend(["white", "beige", "sage_green"])
        elif temp_category in ["warm", "hot"]:
            color_suggestions["primary"].extend(["white", "light_blue", "khaki", "pastels"])
            color_suggestions["accent"].extend(["coral", "yellow", "mint_green"])
            color_suggestions["avoid"].extend(["black", "dark_colors"])
        
        # Precipitation-based adjustments
        if weather_conditions["precipitation"]["category"] in ["moderate", "heavy"]:
            color_suggestions["primary"].extend(["dark_colors", "waterproof_fabrics"])
            color_suggestions["avoid"].extend(["white", "light_colors"])
        
        return color_suggestions
    
    def _recommend_fabrics(self, temperature: float, precipitation: float, wind_speed: float) -> List[Dict[str, Any]]:
        """Recommend appropriate fabrics based on weather conditions."""
        
        fabric_recommendations = []
        
        # Temperature-based fabric recommendations
        if temperature < 10:
            fabric_recommendations.extend([
                {"fabric": "wool", "reason": "Excellent insulation", "priority": "high"},
                {"fabric": "cashmere", "reason": "Warm and soft", "priority": "medium"},
                {"fabric": "fleece", "reason": "Lightweight warmth", "priority": "medium"}
            ])
        elif temperature > 25:
            fabric_recommendations.extend([
                {"fabric": "cotton", "reason": "Breathable and cool", "priority": "high"},
                {"fabric": "linen", "reason": "Natural cooling", "priority": "high"},
                {"fabric": "bamboo", "reason": "Moisture-wicking", "priority": "medium"}
            ])
        else:
            fabric_recommendations.extend([
                {"fabric": "cotton", "reason": "Comfortable and versatile", "priority": "high"},
                {"fabric": "polyester", "reason": "Durable and easy-care", "priority": "medium"}
            ])
        
        # Precipitation-based recommendations
        if precipitation > 5:
            fabric_recommendations.extend([
                {"fabric": "gore_tex", "reason": "Waterproof and breathable", "priority": "high"},
                {"fabric": "nylon", "reason": "Water-resistant", "priority": "medium"}
            ])
        
        # Wind-based recommendations
        if wind_speed > 7:
            fabric_recommendations.extend([
                {"fabric": "windproof_materials", "reason": "Wind protection", "priority": "high"}
            ])
        
        return fabric_recommendations
    
    def _calculate_comfort_score(self, temperature: float, precipitation: float, wind_speed: float) -> float:
        """Calculate overall comfort score for the weather conditions."""
        
        # Temperature comfort (0-100)
        temp_comfort = 100 - abs(temperature - 22) * 2  # Optimal around 22°C
        temp_comfort = max(0, min(100, temp_comfort))
        
        # Precipitation comfort (0-100)
        precip_comfort = max(0, 100 - precipitation * 3)  # Less rain = more comfort
        
        # Wind comfort (0-100)
        wind_comfort = max(0, 100 - wind_speed * 5)  # Less wind = more comfort
        
        # Weighted average
        comfort_score = (temp_comfort * 0.5 + precip_comfort * 0.3 + wind_comfort * 0.2)
        
        return round(comfort_score, 1)
    
    def _generate_style_notes(self, weather_conditions: Dict, style_preference: str, occasion: str) -> List[str]:
        """Generate style notes and tips."""
        
        notes = []
        
        # Weather-specific notes
        if weather_conditions["precipitation"]["category"] in ["moderate", "heavy"]:
            notes.append("Choose waterproof or water-resistant materials")
            notes.append("Consider darker colors that won't show water spots")
        
        if weather_conditions["temperature"]["category"] in ["hot"]:
            notes.append("Opt for loose, breathable fabrics")
            notes.append("Light colors will help reflect heat")
        
        if weather_conditions["wind"]["category"] in ["windy"]:
            notes.append("Secure loose items and avoid flowy fabrics")
            notes.append("Consider a wind-resistant outer layer")
        
        # Style-specific notes
        if style_preference == "business":
            notes.append("Maintain professional appearance despite weather")
            notes.append("Layer appropriately for temperature changes")
        
        if occasion == "formal":
            notes.append("Balance weather protection with formal requirements")
            notes.append("Consider elegant outerwear options")
        
        return notes
    
    # Helper methods for categorization and assessment
    def _categorize_temperature(self, temperature: float) -> str:
        """Categorize temperature for styling purposes."""
        for category, data in self.STYLING_RULES["temperature"].items():
            if data["range"][0] <= temperature < data["range"][1]:
                return category
        return "mild"
    
    def _categorize_sunlight(self, sunlight: float) -> str:
        """Categorize sunlight level."""
        for category, data in self.STYLING_RULES["sunlight"].items():
            if data["range"][0] <= sunlight < data["range"][1]:
                return category
        return "moderate"
    
    def _categorize_precipitation(self, precipitation: float) -> str:
        """Categorize precipitation level."""
        for category, data in self.STYLING_RULES["precipitation"].items():
            if data["range"][0] <= precipitation < data["range"][1]:
                return category
        return "none"
    
    def _categorize_wind(self, wind_speed: float) -> str:
        """Categorize wind speed."""
        for category, data in self.STYLING_RULES["wind"].items():
            if data["range"][0] <= wind_speed < data["range"][1]:
                return category
        return "calm"
    
    def _get_temperature_description(self, temperature: float) -> str:
        """Get human-readable temperature description."""
        if temperature < 0:
            return "Freezing"
        elif temperature < 10:
            return "Cold"
        elif temperature < 18:
            return "Cool"
        elif temperature < 25:
            return "Mild"
        elif temperature < 30:
            return "Warm"
        else:
            return "Hot"
    
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
    
    def _get_wind_description(self, wind_speed: float) -> str:
        """Get human-readable wind description."""
        if wind_speed < 3:
            return "Calm"
        elif wind_speed < 7:
            return "Light breeze"
        elif wind_speed < 15:
            return "Windy"
        else:
            return "Very windy"
    
    def _assess_uv_level(self, sunlight: float) -> str:
        """Assess UV level based on sunlight."""
        if sunlight < 3:
            return "Low"
        elif sunlight < 6:
            return "Moderate"
        elif sunlight < 8:
            return "High"
        else:
            return "Very High"
    
    def _needs_outerwear(self, temperature: float, precipitation: float, wind_speed: float) -> bool:
        """Determine if outerwear is needed."""
        return (temperature < 15 or precipitation > 2 or wind_speed > 5)
    
    def _needs_layering(self, temperature: float, wind_speed: float) -> bool:
        """Determine if layering is recommended."""
        return (10 <= temperature <= 20 or wind_speed > 3)
    
    def _get_season(self) -> str:
        """Get current season (simplified)."""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"
    
    def _assess_item_weather_suitability(self, item_data: Dict, temperature: float, precipitation: float) -> str:
        """Assess how well an item suits current weather."""
        temp_suitable = (item_data.get("temp_range", (0, 40))[0] <= temperature <= item_data.get("temp_range", (0, 40))[1])
        precip_suitable = precipitation < 5 or "rain" in item_data.get("conditions", [])
        
        if temp_suitable and precip_suitable:
            return "excellent"
        elif temp_suitable or precip_suitable:
            return "good"
        else:
            return "poor"
    
    def _assess_style_match(self, item_data: Dict, style_preference: str) -> str:
        """Assess how well an item matches style preference."""
        if style_preference in item_data.get("occasions", []):
            return "excellent"
        elif "casual" in item_data.get("occasions", []) and style_preference == "casual":
            return "good"
        else:
            return "fair"
    
    def _calculate_outfit_comfort(self, items: List[Dict], temperature: float, wind_speed: float) -> float:
        """Calculate overall outfit comfort score."""
        if not items:
            return 0
        
        total_score = 0
        for item in items:
            weather_suitability = item.get("weather_suitability", "fair")
            if weather_suitability == "excellent":
                total_score += 100
            elif weather_suitability == "good":
                total_score += 75
            else:
                total_score += 50
        
        return round(total_score / len(items), 1)
    
    def _calculate_outfit_style(self, items: List[Dict], style_preference: str, occasion: str) -> float:
        """Calculate overall outfit style score."""
        if not items:
            return 0
        
        total_score = 0
        for item in items:
            style_match = item.get("style_match", "fair")
            if style_match == "excellent":
                total_score += 100
            elif style_match == "good":
                total_score += 75
            else:
                total_score += 50
        
        return round(total_score / len(items), 1)
    
    def _calculate_weather_appropriateness(self, items: List[Dict], temperature: float, 
                                         precipitation: float, wind_speed: float) -> float:
        """Calculate how appropriate the outfit is for current weather."""
        if not items:
            return 0
        
        total_score = 0
        for item in items:
            weather_suitability = item.get("weather_suitability", "fair")
            if weather_suitability == "excellent":
                total_score += 100
            elif weather_suitability == "good":
                total_score += 75
            else:
                total_score += 50
        
        return round(total_score / len(items), 1)
    
    def _generate_outfit_notes(self, items: List[Dict], temperature: float, 
                             precipitation: float, wind_speed: float) -> List[str]:
        """Generate specific notes for the outfit."""
        notes = []
        
        # Check for weather mismatches
        for item in items:
            if item.get("weather_suitability") == "poor":
                notes.append(f"Consider replacing {item['name']} for better weather protection")
        
        # Add general weather notes
        if precipitation > 5:
            notes.append("Ensure all items are water-resistant or waterproof")
        
        if temperature < 10:
            notes.append("Layer appropriately for warmth")
        
        if wind_speed > 7:
            notes.append("Secure loose items against wind")
        
        return notes


# Create a global instance for easy import
fashion_rules = FashionStylist()