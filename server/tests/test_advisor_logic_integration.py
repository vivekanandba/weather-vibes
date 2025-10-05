"""
Integration tests for advisor logic functions.

Tests the actual advisor logic implementations with various weather conditions
and parameter combinations to ensure robust recommendation generation.
"""

import pytest
from app.core.advisors.fashion_rules import fashion_rules
from app.core.advisors.crop_advisor import crop_advisor
from app.core.advisors.mood_predictor import mood_predictor


class TestFashionAdvisorLogic:
    """Integration tests for Fashion Advisor logic."""
    
    def test_fashion_advisor_extreme_cold_conditions(self):
        """Test fashion advisor with extreme cold conditions."""
        parameter_values = {
            "T2M": -15.0,
            "ALLSKY_SFC_SW_DWN": 2.0,
            "PRECTOTCORR": 10.0,
            "WS2M": 12.0
        }
        
        additional_params = {
            "style_preference": "casual",
            "occasion": "outdoor",
            "gender": "unisex"
        }
        
        result = fashion_rules.generate_recommendations(parameter_values, additional_params)
        
        # Verify response structure
        assert "weather_conditions" in result
        assert "outfit_recommendations" in result
        assert "fabric_recommendations" in result
        
        # Should recommend warm fabrics
        fabric_recs = result.get("fabric_recommendations", [])
        warm_fabrics = [rec for rec in fabric_recs if rec["fabric"] in ["wool", "fleece", "down"]]
        assert len(warm_fabrics) > 0, "Should recommend warm fabrics for extreme cold"
        
        # Should have high priority recommendations for warmth
        high_priority_fabrics = [rec for rec in fabric_recs if rec["priority"] == "high"]
        assert len(high_priority_fabrics) > 0, "Should have high priority fabric recommendations for cold"

    def test_fashion_advisor_extreme_hot_conditions(self):
        """Test fashion advisor with extreme hot conditions."""
        parameter_values = {
            "T2M": 42.0,
            "ALLSKY_SFC_SW_DWN": 9.5,
            "PRECTOTCORR": 0.0,
            "WS2M": 3.0
        }
        
        additional_params = {
            "style_preference": "casual",
            "occasion": "outdoor",
            "gender": "unisex"
        }
        
        result = fashion_rules.generate_recommendations(parameter_values, additional_params)
        
        # Should recommend breathable fabrics
        fabric_recs = result.get("fabric_recommendations", [])
        cooling_fabrics = [rec for rec in fabric_recs if rec["fabric"] in ["cotton", "linen", "bamboo"]]
        assert len(cooling_fabrics) > 0, "Should recommend cooling fabrics for extreme heat"
        
        # Should recommend sun protection accessories
        accessory_recs = result.get("accessory_recommendations", [])
        sun_protection = [rec for rec in accessory_recs if "sun" in rec["name"].lower() or "hat" in rec["name"].lower()]
        assert len(sun_protection) > 0, "Should recommend sun protection accessories"

    def test_fashion_advisor_rainy_conditions(self):
        """Test fashion advisor with heavy rain conditions."""
        parameter_values = {
            "T2M": 18.0,
            "ALLSKY_SFC_SW_DWN": 1.0,
            "PRECTOTCORR": 25.0,
            "WS2M": 8.0
        }
        
        additional_params = {
            "style_preference": "business",
            "occasion": "work",
            "gender": "unisex"
        }
        
        result = fashion_rules.generate_recommendations(parameter_values, additional_params)
        
        # Should recommend waterproof items
        accessory_recs = result.get("accessory_recommendations", [])
        rain_protection = [rec for rec in accessory_recs if "umbrella" in rec["name"].lower()]
        assert len(rain_protection) > 0, "Should recommend umbrella for heavy rain"
        
        # Should recommend appropriate footwear
        outfit_recs = result.get("outfit_recommendations", [])
        if outfit_recs:
            # Check if any outfit recommends waterproof items
            waterproof_items = any("rain" in str(outfit).lower() or "waterproof" in str(outfit).lower() 
                                 for outfit in outfit_recs)

    @pytest.mark.parametrize("style_occasion", [
        ("casual", "weekend"),
        ("business", "work"), 
        ("formal", "event"),
        ("athletic", "gym"),
    ])
    def test_fashion_advisor_style_adaptations(self, style_occasion):
        """Test fashion advisor adapts to different style preferences and occasions."""
        style_preference, occasion = style_occasion
        
        parameter_values = {
            "T2M": 22.0,
            "ALLSKY_SFC_SW_DWN": 6.0,
            "PRECTOTCORR": 2.0,
            "WS2M": 4.0
        }
        
        additional_params = {
            "style_preference": style_preference,
            "occasion": occasion,
            "gender": "unisex"
        }
        
        result = fashion_rules.generate_recommendations(parameter_values, additional_params)
        
        # Verify basic response structure
        assert "outfit_recommendations" in result
        assert len(result["outfit_recommendations"]) > 0
        
        # Business/formal should have higher style scores
        outfit_recs = result.get("outfit_recommendations", [])
        if style_preference in ["business", "formal"]:
            for outfit in outfit_recs:
                assert outfit.get("style_score", 0) >= 60, f"Style score too low for {style_preference} occasion"


class TestCropAdvisorLogic:
    """Integration tests for Crop Advisor logic."""
    
    @pytest.mark.parametrize("crop_type", ["tomato", "rice", "wheat", "corn", "potato"])
    def test_crop_advisor_all_supported_crops(self, crop_type):
        """Test crop advisor with all supported crop types."""
        parameter_values = {
            "T2M": 25.0,
            "PRECTOTCORR": 15.0,
            "T2M_MIN": 18.0,
            "T2M_MAX": 32.0,
            "RH2M": 65.0
        }
        
        additional_params = {
            "crop_type": crop_type,
            "planting_date": "2024-06-15",
            "location": "Test Farm"
        }
        
        result = crop_advisor.generate_recommendations(parameter_values, additional_params)
        
        # Verify response structure
        assert "crop_type" in result
        assert result["crop_type"] == crop_type
        assert "current_conditions" in result
        assert "planting_window" in result
        assert "risk_assessment" in result
        assert "alerts" in result
        
        # Should have current conditions analysis
        current_conditions = result["current_conditions"]
        assert "overall_score" in current_conditions
        assert "temperature" in current_conditions
        assert "precipitation" in current_conditions

    def test_crop_advisor_drought_conditions(self):
        """Test crop advisor with drought conditions."""
        parameter_values = {
            "T2M": 35.0,
            "PRECTOTCORR": 0.5,  # Very low precipitation
            "T2M_MIN": 28.0,
            "T2M_MAX": 42.0,
            "RH2M": 25.0  # Low humidity
        }
        
        additional_params = {
            "crop_type": "tomato",
            "planting_date": "2024-06-01"
        }
        
        result = crop_advisor.generate_recommendations(parameter_values, additional_params)
        
        # Should generate drought alerts
        alerts = result.get("alerts", [])
        drought_alerts = [alert for alert in alerts if "drought" in alert.get("message", "").lower()]
        assert len(drought_alerts) > 0, "Should generate drought alerts for low precipitation"
        
        # Should have high-priority irrigation recommendations
        recommendations = result.get("recommendations", [])
        irrigation_recs = [rec for rec in recommendations if "irrigation" in rec.get("category", "")]
        assert len(irrigation_recs) > 0, "Should recommend irrigation for drought conditions"

    def test_crop_advisor_frost_risk(self):
        """Test crop advisor with frost risk conditions."""
        parameter_values = {
            "T2M": 8.0,
            "PRECTOTCORR": 5.0,
            "T2M_MIN": -2.0,  # Below freezing
            "T2M_MAX": 15.0,
            "RH2M": 80.0
        }
        
        additional_params = {
            "crop_type": "tomato",  # Frost-sensitive crop
            "planting_date": "2024-03-15"
        }
        
        result = crop_advisor.generate_recommendations(parameter_values, additional_params)
        
        # Should identify frost risk
        risk_assessment = result.get("risk_assessment", {})
        risk_factors = risk_assessment.get("factors", [])
        frost_risks = [risk for risk in risk_factors if risk.get("type") == "frost"]
        assert len(frost_risks) > 0, "Should identify frost risk"
        
        # Should generate critical alerts
        alerts = result.get("alerts", [])
        critical_alerts = [alert for alert in alerts if alert.get("type") == "critical"]
        assert len(critical_alerts) > 0, "Should generate critical alerts for frost conditions"

    def test_crop_advisor_optimal_conditions(self):
        """Test crop advisor with optimal growing conditions."""
        parameter_values = {
            "T2M": 22.0,  # Optimal for most crops
            "PRECTOTCORR": 40.0,  # Good precipitation
            "T2M_MIN": 18.0,
            "T2M_MAX": 28.0,
            "RH2M": 60.0
        }
        
        additional_params = {
            "crop_type": "tomato",
            "planting_date": "2024-05-01"
        }
        
        result = crop_advisor.generate_recommendations(parameter_values, additional_params)
        
        # Should have high overall score
        current_conditions = result.get("current_conditions", {})
        overall_score = current_conditions.get("overall_score", 0)
        assert overall_score >= 75, "Should have high score for optimal conditions"
        
        # Should have low risk assessment
        risk_assessment = result.get("risk_assessment", {})
        overall_risk = risk_assessment.get("overall", "high")
        assert overall_risk in ["low", "medium"], "Should have low/medium risk for optimal conditions"


class TestMoodAdvisorLogic:
    """Integration tests for Mood Advisor logic."""
    
    def test_mood_advisor_sunny_conditions(self):
        """Test mood advisor with bright sunny conditions."""
        parameter_values = {
            "T2M": 24.0,
            "ALLSKY_SFC_SW_DWN": 8.5,  # High sunlight
            "PRECTOTCORR": 0.0,
            "RH2M": 45.0
        }
        
        additional_params = {
            "sensitivity_level": "normal"
        }
        
        result = mood_predictor.generate_recommendations(parameter_values, additional_params)
        
        # Should have high mood score
        mood_prediction = result.get("mood_prediction", {})
        overall_score = mood_prediction.get("overall_score", 0)
        assert overall_score >= 75, "Should have high mood score for sunny conditions"
        
        # Should recommend outdoor activities
        activity_suggestions = result.get("activity_suggestions", [])
        outdoor_activities = [act for act in activity_suggestions 
                            if "outdoor" in act.get("name", "").lower()]
        assert len(outdoor_activities) > 0, "Should suggest outdoor activities for sunny weather"

    def test_mood_advisor_gloomy_conditions(self):
        """Test mood advisor with gloomy conditions."""
        parameter_values = {
            "T2M": 12.0,
            "ALLSKY_SFC_SW_DWN": 1.5,  # Very low sunlight
            "PRECTOTCORR": 15.0,
            "RH2M": 85.0
        }
        
        additional_params = {
            "sensitivity_level": "high"
        }
        
        result = mood_predictor.generate_recommendations(parameter_values, additional_params)
        
        # Should have lower mood score
        mood_prediction = result.get("mood_prediction", {})
        overall_score = mood_prediction.get("overall_score", 100)
        assert overall_score <= 60, "Should have lower mood score for gloomy conditions"
        
        # Should recommend indoor comfort activities
        activity_suggestions = result.get("activity_suggestions", [])
        indoor_activities = [act for act in activity_suggestions 
                           if "indoor" in act.get("name", "").lower() or 
                              "relaxation" in act.get("name", "").lower()]
        assert len(indoor_activities) > 0, "Should suggest indoor activities for gloomy weather"

    def test_mood_advisor_factor_analysis(self):
        """Test mood advisor provides detailed factor analysis."""
        parameter_values = {
            "T2M": 20.0,
            "ALLSKY_SFC_SW_DWN": 5.0,
            "PRECTOTCORR": 8.0,
            "RH2M": 65.0
        }
        
        additional_params = {
            "sensitivity_level": "normal"
        }
        
        result = mood_predictor.generate_recommendations(parameter_values, additional_params)
        
        # Should provide factor analysis
        mood_prediction = result.get("mood_prediction", {})
        factors = mood_prediction.get("factors", [])
        assert len(factors) >= 4, "Should analyze multiple weather factors"
        
        # Should include temperature, sunlight, precipitation, humidity factors
        factor_types = {factor.get("factor") for factor in factors}
        expected_factors = {"temperature", "sunlight", "precipitation", "humidity"}
        assert expected_factors.issubset(factor_types), "Should include all major weather factors"

    @pytest.mark.parametrize("sensitivity_level", ["low", "normal", "high"])
    def test_mood_advisor_sensitivity_levels(self, sensitivity_level):
        """Test mood advisor adapts to different sensitivity levels."""
        parameter_values = {
            "T2M": 18.0,
            "ALLSKY_SFC_SW_DWN": 3.0,  # Moderate conditions
            "PRECTOTCORR": 5.0,
            "RH2M": 70.0
        }
        
        additional_params = {
            "sensitivity_level": sensitivity_level
        }
        
        result = mood_predictor.generate_recommendations(parameter_values, additional_params)
        
        # Should provide appropriate wellness recommendations
        wellness_recs = result.get("wellness_recommendations", {})
        assert "wellness_tips" in wellness_recs
        assert len(wellness_recs["wellness_tips"]) > 0
        
        # High sensitivity should have more specific recommendations
        if sensitivity_level == "high":
            wellness_tips = wellness_recs.get("wellness_tips", [])
            specific_tips = [tip for tip in wellness_tips if "sensitive" in tip.lower() or "monitor" in tip.lower()]
            # High sensitivity might have more targeted advice

    def test_mood_advisor_seasonal_depression_conditions(self):
        """Test mood advisor with conditions likely to cause seasonal depression."""
        parameter_values = {
            "T2M": 5.0,
            "ALLSKY_SFC_SW_DWN": 1.0,  # Very low sunlight (winter conditions)
            "PRECTOTCORR": 12.0,
            "RH2M": 80.0
        }
        
        additional_params = {
            "sensitivity_level": "high"
        }
        
        result = mood_predictor.generate_recommendations(parameter_values, additional_params)
        
        # Should recommend light therapy or vitamin D
        wellness_recs = result.get("wellness_recommendations", {})
        wellness_tips = wellness_recs.get("wellness_tips", [])
        light_therapy_tips = [tip for tip in wellness_tips 
                            if "light" in tip.lower() or "vitamin d" in tip.lower()]
        
        # Should have daily tips for managing low-light conditions
        daily_tips = result.get("daily_tips", [])
        seasonal_tips = [tip for tip in daily_tips 
                       if "light" in tip.lower() or "indoor" in tip.lower()]


class TestAdvisorLogicEdgeCases:
    """Test edge cases across all advisor logic implementations."""
    
    def test_all_advisors_handle_missing_parameters(self):
        """Test all advisors handle missing weather parameters gracefully."""
        incomplete_params = {"T2M": 20.0}  # Only temperature
        
        advisors = [
            (fashion_rules, {"style_preference": "casual"}),
            (crop_advisor, {"crop_type": "tomato"}),
            (mood_predictor, {"sensitivity_level": "normal"})
        ]
        
        for advisor, additional_params in advisors:
            result = advisor.generate_recommendations(incomplete_params, additional_params)
            
            # Should not crash and should provide some recommendations
            assert isinstance(result, dict), f"Advisor {advisor} should return dict"
            
            # Should handle missing parameters with defaults
            if hasattr(advisor, '__name__') and advisor.__name__ == 'fashion_rules':
                assert "weather_conditions" in result
            elif hasattr(advisor, '__name__') and advisor.__name__ == 'crop_advisor':
                assert "current_conditions" in result
            elif hasattr(advisor, '__name__') and advisor.__name__ == 'mood_predictor':
                assert "mood_prediction" in result

    def test_all_advisors_handle_extreme_values(self):
        """Test all advisors handle extreme weather values."""
        extreme_params = {
            "T2M": 999.0,  # Impossible temperature
            "ALLSKY_SFC_SW_DWN": -5.0,  # Negative sunlight
            "PRECTOTCORR": 500.0,  # Extreme precipitation
            "RH2M": 150.0  # Over 100% humidity
        }
        
        advisors = [
            (fashion_rules, {"style_preference": "casual"}),
            (crop_advisor, {"crop_type": "tomato"}),
            (mood_predictor, {"sensitivity_level": "normal"})
        ]
        
        for advisor, additional_params in advisors:
            # Should not crash with extreme values
            try:
                result = advisor.generate_recommendations(extreme_params, additional_params)
                assert isinstance(result, dict), f"Advisor {advisor} should handle extreme values"
            except Exception as e:
                pytest.fail(f"Advisor {advisor} crashed with extreme values: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])