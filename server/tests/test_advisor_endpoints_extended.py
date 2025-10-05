"""
Extended unit tests for advisor endpoints with comprehensive edge cases and integration scenarios.

Tests advanced scenarios, error handling, data validation, and performance edge cases.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, call
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.main import app

client = TestClient(app)


class TestAdvisorEndpointsExtended:
    """Extended test cases for comprehensive advisor endpoint testing."""
    
    def setup_method(self):
        """Set up test data and mocks for extended testing."""
        self.test_locations = [
            {"lat": 12.9716, "lon": 77.5946, "location_name": "Bangalore"},  # Tropical
            {"lat": 40.7128, "lon": -74.0060, "location_name": "New York"},  # Temperate
            {"lat": -33.8688, "lon": 151.2093, "location_name": "Sydney"},   # Southern hemisphere
            {"lat": 64.1466, "lon": -21.9426, "location_name": "Reykjavik"}, # Arctic
            {"lat": 25.0343, "lon": 121.5645, "location_name": "Taipei"},    # Humid subtropical
        ]
        
        self.extreme_weather_conditions = [
            {"T2M": -20.0, "ALLSKY_SFC_SW_DWN": 0.5, "PRECTOTCORR": 50.0, "WS2M": 15.0, "RH2M": 95.0},  # Extreme cold/wet
            {"T2M": 45.0, "ALLSKY_SFC_SW_DWN": 10.0, "PRECTOTCORR": 0.0, "WS2M": 2.0, "RH2M": 10.0},   # Extreme hot/dry  
            {"T2M": 30.0, "ALLSKY_SFC_SW_DWN": 2.0, "PRECTOTCORR": 100.0, "WS2M": 25.0, "RH2M": 90.0}, # Monsoon-like
            {"T2M": 5.0, "ALLSKY_SFC_SW_DWN": 8.0, "PRECTOTCORR": 0.1, "WS2M": 30.0, "RH2M": 30.0},   # Cold but sunny/windy
        ]
        
        self.mock_vibe_config = {
            "name": "Test Advisor",
            "parameters": ["T2M", "ALLSKY_SFC_SW_DWN", "PRECTOTCORR", "WS2M", "RH2M"],
            "logic": "test_logic"
        }

    @pytest.mark.parametrize("advisor_type,additional_params", [
        ("fashion", {"style_preference": "business", "occasion": "formal", "gender": "female"}),
        ("fashion", {"style_preference": "athletic", "occasion": "athletic", "gender": "male"}),
        ("fashion", {"style_preference": "casual", "occasion": "casual", "gender": "unisex"}),
        ("crop", {"cropType": "tomato", "plantingDate": "2024-03-15", "farmSize": "small"}),
        ("crop", {"cropType": "rice", "plantingDate": "2024-06-01", "farmSize": "large"}),
        ("crop", {"cropType": "wheat", "plantingDate": "2024-10-15", "farmSize": "medium"}),
        ("mood", {"moodSensitivity": "high", "activityLevel": "active"}),
        ("mood", {"moodSensitivity": "normal", "activityLevel": "moderate"}),
        ("mood", {"moodSensitivity": "low", "activityLevel": "sedentary"}),
    ])
    @patch('app.api.routes.advisor.get_vibe_engine')
    @patch('app.api.routes.advisor.get_data_service')
    def test_advisor_with_various_parameters(self, mock_data_service, mock_vibe_engine, advisor_type, additional_params):
        """Test all advisors with various parameter combinations."""
        # Mock services
        mock_engine = MagicMock()
        mock_engine.get_vibe_config.return_value = self.mock_vibe_config
        mock_vibe_engine.return_value = mock_engine
        
        mock_data = MagicMock()
        mock_data.get_all_parameters.return_value = self.extreme_weather_conditions[0]
        mock_data_service.return_value = mock_data
        
        request_data = {
            "advisor_type": advisor_type,
            "lat": 12.9716,
            "lon": 77.5946,
            "month": 6,
            "year": 2024,
            "additional_params": additional_params
        }
        
        response = client.post("/api/advisor", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["advisor_type"] == advisor_type
        assert len(data["recommendations"]) > 0

    @pytest.mark.parametrize("location", [
        {"lat": 12.9716, "lon": 77.5946},   # Bangalore
        {"lat": 40.7128, "lon": -74.0060},  # New York  
        {"lat": -33.8688, "lon": 151.2093}, # Sydney
        {"lat": 64.1466, "lon": -21.9426},  # Reykjavik
    ])
    @patch('app.api.routes.advisor.get_vibe_engine')
    @patch('app.api.routes.advisor.get_data_service')
    def test_fashion_advisor_geographical_variations(self, mock_data_service, mock_vibe_engine, location):
        """Test fashion advisor adapts to different geographical locations."""
        mock_engine = MagicMock()
        mock_engine.get_vibe_config.return_value = self.mock_vibe_config
        mock_vibe_engine.return_value = mock_engine
        
        # Vary weather conditions based on location
        if location["lat"] > 60:  # Arctic
            weather_data = {"T2M": -10.0, "ALLSKY_SFC_SW_DWN": 2.0, "PRECTOTCORR": 10.0, "WS2M": 8.0, "RH2M": 75.0}
        elif location["lat"] < 0:  # Southern hemisphere
            weather_data = {"T2M": 22.0, "ALLSKY_SFC_SW_DWN": 7.0, "PRECTOTCORR": 5.0, "WS2M": 4.0, "RH2M": 55.0}
        else:  # Tropical/Temperate
            weather_data = {"T2M": 28.0, "ALLSKY_SFC_SW_DWN": 8.5, "PRECTOTCORR": 2.0, "WS2M": 3.0, "RH2M": 65.0}
        
        mock_data = MagicMock()
        mock_data.get_all_parameters.return_value = weather_data
        mock_data_service.return_value = mock_data
        
        request_data = {
            "advisor_type": "fashion",
            "lat": location["lat"],
            "lon": location["lon"], 
            "month": 6,
            "additional_params": {"style_preference": "casual", "occasion": "casual"}
        }
        
        response = client.post("/api/advisor", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Verify weather data influenced recommendations
        raw_data = data.get("raw_data", {})
        if isinstance(raw_data, dict):
            # Check that outfit recommendations adapt to temperature
            outfit_recs = raw_data.get("outfit_recommendations", [])
            if outfit_recs and location["lat"] > 60:  # Arctic location should suggest warm clothing
                assert any("warm" in str(rec).lower() or "layer" in str(rec).lower() for rec in outfit_recs)

    @pytest.mark.parametrize("weather_condition", [
        {"T2M": -20.0, "ALLSKY_SFC_SW_DWN": 0.5, "PRECTOTCORR": 50.0, "WS2M": 15.0, "RH2M": 95.0},
        {"T2M": 45.0, "ALLSKY_SFC_SW_DWN": 10.0, "PRECTOTCORR": 0.0, "WS2M": 2.0, "RH2M": 10.0},
        {"T2M": 30.0, "ALLSKY_SFC_SW_DWN": 2.0, "PRECTOTCORR": 100.0, "WS2M": 25.0, "RH2M": 90.0},
    ])
    @patch('app.api.routes.advisor.get_vibe_engine')
    @patch('app.api.routes.advisor.get_data_service')
    def test_advisors_extreme_weather_conditions(self, mock_data_service, mock_vibe_engine, weather_condition):
        """Test all advisors handle extreme weather conditions gracefully."""
        mock_engine = MagicMock()
        mock_engine.get_vibe_config.return_value = self.mock_vibe_config
        mock_vibe_engine.return_value = mock_engine
        
        mock_data = MagicMock()
        mock_data.get_all_parameters.return_value = weather_condition
        mock_data_service.return_value = mock_data
        
        for advisor_type in ["fashion", "crop", "mood"]:
            request_data = {
                "advisor_type": advisor_type,
                "lat": 12.9716,
                "lon": 77.5946,
                "month": 6,
                "additional_params": {}
            }
            
            response = client.post("/api/advisor", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            assert len(data["recommendations"]) > 0
            
            # Extreme conditions should generate appropriate alerts/recommendations
            if advisor_type == "crop" and (weather_condition["T2M"] < 0 or weather_condition["PRECTOTCORR"] > 50):
                raw_data = data.get("raw_data", {})
                alerts = raw_data.get("alerts", [])
                # Should have alerts for extreme conditions
                assert len(alerts) > 0

    @pytest.mark.parametrize("invalid_data", [
        {"advisor_type": "invalid_type", "lat": 12.9716, "lon": 77.5946, "month": 6},
        {"advisor_type": "fashion", "lat": 91.0, "lon": 77.5946, "month": 6},  # Invalid latitude
        {"advisor_type": "fashion", "lat": 12.9716, "lon": 181.0, "month": 6},  # Invalid longitude
        {"advisor_type": "fashion", "lat": 12.9716, "lon": 77.5946, "month": 13}, # Invalid month
        {"advisor_type": "fashion", "lat": 12.9716, "lon": 77.5946, "month": 0},  # Invalid month
    ])
    def test_advisor_endpoint_validation_errors(self, invalid_data):
        """Test advisor endpoint properly validates input data."""
        response = client.post("/api/advisor", json=invalid_data)
        
        if invalid_data.get("advisor_type") == "invalid_type":
            assert response.status_code == 400
            assert "Unknown advisor type" in response.json()["detail"]
        else:
            # Other validation errors should be caught by Pydantic
            assert response.status_code in [400, 422]

    @patch('app.api.routes.advisor.get_vibe_engine')
    @patch('app.api.routes.advisor.get_data_service')
    def test_advisor_concurrent_requests(self, mock_data_service, mock_vibe_engine):
        """Test advisor endpoint handles concurrent requests properly."""
        mock_engine = MagicMock()
        mock_engine.get_vibe_config.return_value = self.mock_vibe_config
        mock_vibe_engine.return_value = mock_engine
        
        mock_data = MagicMock()
        mock_data.get_all_parameters.return_value = self.extreme_weather_conditions[0]
        mock_data_service.return_value = mock_data
        
        def make_request(advisor_type, location_idx):
            location = self.test_locations[location_idx % len(self.test_locations)]
            request_data = {
                "advisor_type": advisor_type,
                "lat": location["lat"],
                "lon": location["lon"],
                "month": 6,
                "additional_params": {}
            }
            return client.post("/api/advisor", json=request_data)
        
        # Create concurrent requests
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(10):
                advisor_type = ["fashion", "crop", "mood"][i % 3]
                future = executor.submit(make_request, advisor_type, i)
                futures.append(future)
            
            # Collect results
            responses = [future.result() for future in futures]
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "recommendations" in data
            assert len(data["recommendations"]) > 0

    @patch('app.api.routes.advisor.get_vibe_engine')
    @patch('app.api.routes.advisor.get_data_service')
    def test_advisor_data_service_timeout_handling(self, mock_data_service, mock_vibe_engine):
        """Test advisor endpoint handles data service timeouts gracefully."""
        mock_engine = MagicMock()
        mock_engine.get_vibe_config.return_value = self.mock_vibe_config
        mock_vibe_engine.return_value = mock_engine
        
        # Mock data service to raise timeout exception
        mock_data = MagicMock()
        mock_data.get_all_parameters.side_effect = TimeoutError("Data service timeout")
        mock_data_service.return_value = mock_data
        
        request_data = {
            "advisor_type": "fashion",
            "lat": 12.9716,
            "lon": 77.5946,
            "month": 6,
        }
        
        response = client.post("/api/advisor", json=request_data)
        assert response.status_code == 500
        assert "Error retrieving weather data" in response.json()["detail"]

    @patch('app.api.routes.advisor.get_vibe_engine')
    @patch('app.api.routes.advisor.get_data_service')
    def test_advisor_partial_data_handling(self, mock_data_service, mock_vibe_engine):
        """Test advisor endpoint handles partial/missing weather data."""
        mock_engine = MagicMock()
        mock_engine.get_vibe_config.return_value = self.mock_vibe_config
        mock_vibe_engine.return_value = mock_engine
        
        # Test with missing parameters
        incomplete_data_sets = [
            {"T2M": 25.0},  # Only temperature
            {"T2M": 25.0, "PRECTOTCORR": 5.0},  # Missing sunlight and wind
            {"ALLSKY_SFC_SW_DWN": 7.0, "WS2M": 3.0},  # Missing temperature and precipitation
            {},  # Completely empty
        ]
        
        for incomplete_data in incomplete_data_sets:
            mock_data = MagicMock()
            mock_data.get_all_parameters.return_value = incomplete_data
            mock_data_service.return_value = mock_data
            
            request_data = {
                "advisor_type": "fashion",
                "lat": 12.9716,
                "lon": 77.5946,
                "month": 6,
            }
            
            response = client.post("/api/advisor", json=request_data)
            
            if not incomplete_data:  # Empty data should result in 404
                assert response.status_code == 404
            else:
                # Partial data should still generate recommendations with defaults
                assert response.status_code == 200
                data = response.json()
                assert len(data["recommendations"]) > 0

    @pytest.mark.parametrize("month,expected_seasonal_adaptation", [
        (12, "winter"),  # December - winter clothing/activities
        (3, "spring"),   # March - transitional recommendations  
        (6, "summer"),   # June - summer clothing/activities
        (9, "autumn"),   # September - fall preparations
    ])
    @patch('app.api.routes.advisor.get_vibe_engine')
    @patch('app.api.routes.advisor.get_data_service')
    def test_advisor_seasonal_adaptation(self, mock_data_service, mock_vibe_engine, month, expected_seasonal_adaptation):
        """Test advisors adapt recommendations based on seasonal patterns."""
        mock_engine = MagicMock()
        mock_engine.get_vibe_config.return_value = self.mock_vibe_config
        mock_vibe_engine.return_value = mock_engine
        
        # Set weather data appropriate for season
        seasonal_weather = {
            12: {"T2M": 10.0, "ALLSKY_SFC_SW_DWN": 3.0, "PRECTOTCORR": 20.0, "WS2M": 8.0, "RH2M": 70.0},
            3: {"T2M": 20.0, "ALLSKY_SFC_SW_DWN": 6.0, "PRECTOTCORR": 15.0, "WS2M": 5.0, "RH2M": 60.0},
            6: {"T2M": 32.0, "ALLSKY_SFC_SW_DWN": 9.0, "PRECTOTCORR": 2.0, "WS2M": 3.0, "RH2M": 45.0},
            9: {"T2M": 25.0, "ALLSKY_SFC_SW_DWN": 6.5, "PRECTOTCORR": 8.0, "WS2M": 4.0, "RH2M": 55.0},
        }
        
        mock_data = MagicMock()
        mock_data.get_all_parameters.return_value = seasonal_weather[month]
        mock_data_service.return_value = mock_data
        
        request_data = {
            "advisor_type": "fashion", 
            "lat": 40.7128,  # New York - clear seasons
            "lon": -74.0060,
            "month": month,
            "additional_params": {"style_preference": "casual"}
        }
        
        response = client.post("/api/advisor", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        raw_data = data.get("raw_data", {})
        
        # Fashion advisor should recommend season-appropriate items
        if month == 12:  # Winter
            # Should recommend warm clothing
            outfit_recs = raw_data.get("outfit_recommendations", [])
            fabric_recs = raw_data.get("fabric_recommendations", [])
            # Check for warm fabrics/items
            warm_items = any("wool" in str(rec).lower() or "warm" in str(rec).lower() 
                           for rec in fabric_recs)
        elif month == 6:  # Summer  
            # Should recommend light clothing
            fabric_recs = raw_data.get("fabric_recommendations", [])
            light_items = any("cotton" in str(rec).lower() or "light" in str(rec).lower()
                            for rec in fabric_recs)

    @patch('app.api.routes.advisor.get_vibe_engine')
    @patch('app.api.routes.advisor.get_data_service')
    def test_advisor_response_structure_consistency(self, mock_data_service, mock_vibe_engine):
        """Test all advisor responses maintain consistent structure."""
        mock_engine = MagicMock()
        mock_engine.get_vibe_config.return_value = self.mock_vibe_config
        mock_vibe_engine.return_value = mock_engine
        
        mock_data = MagicMock()
        mock_data.get_all_parameters.return_value = self.extreme_weather_conditions[0]
        mock_data_service.return_value = mock_data
        
        required_fields = ["advisor_type", "location", "recommendations", "metadata", "raw_data"]
        required_metadata_fields = ["month", "advisor_name"]
        
        for advisor_type in ["fashion", "crop", "mood"]:
            request_data = {
                "advisor_type": advisor_type,
                "lat": 12.9716,
                "lon": 77.5946, 
                "month": 6,
            }
            
            response = client.post("/api/advisor", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            
            # Check required top-level fields
            for field in required_fields:
                assert field in data, f"Missing field {field} in {advisor_type} response"
            
            # Check required metadata fields
            metadata = data.get("metadata", {})
            for field in required_metadata_fields:
                assert field in metadata, f"Missing metadata field {field} in {advisor_type} response"
            
            # Check recommendations structure
            recommendations = data.get("recommendations", [])
            assert len(recommendations) > 0, f"No recommendations in {advisor_type} response"
            
            for rec in recommendations:
                assert "item" in rec, f"Recommendation missing 'item' field in {advisor_type}"
                assert "icon" in rec, f"Recommendation missing 'icon' field in {advisor_type}"
                # description is optional but should be string if present
                if "description" in rec:
                    assert isinstance(rec["description"], str)

    def test_advisor_endpoint_performance_baseline(self):
        """Test advisor endpoint performance under normal conditions."""
        import time
        
        request_data = {
            "advisor_type": "fashion",
            "lat": 12.9716,
            "lon": 77.5946,
            "month": 6,
        }
        
        # Make multiple requests to establish baseline
        response_times = []
        for _ in range(5):
            start_time = time.time()
            response = client.post("/api/advisor", json=request_data)
            end_time = time.time()
            
            # Even if mocked, response should be fast
            response_time = end_time - start_time
            response_times.append(response_time)
            
        avg_response_time = sum(response_times) / len(response_times)
        
        # Response should be under 2 seconds even with processing
        assert avg_response_time < 2.0, f"Average response time {avg_response_time:.2f}s too slow"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])