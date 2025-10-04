from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
from functools import lru_cache


class DataService:
    """Service for accessing GeoTIFF climate data."""

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.cache: Dict = {}

    def _get_geotiff_path(
        self,
        parameter_id: str,
        month: int,
        year: Optional[int] = None
    ) -> Path:
        """
        Construct path to GeoTIFF file.

        Naming convention:
        - With year: {parameter_id}_{year}_{month:02d}.tif
        - Climatology: {parameter_id}_{month:02d}_climatology.tif
        """
        if year:
            filename = f"{parameter_id}_{year}_{month:02d}.tif"
        else:
            filename = f"{parameter_id}_{month:02d}_climatology.tif"

        return self.data_path / filename

    def load_geotiff(
        self,
        parameter_id: str,
        month: int,
        year: Optional[int] = None
    ):
        """
        Load GeoTIFF file with caching.

        Note: This is a placeholder. Actual implementation will use rasterio
        when GeoTIFF files are available.
        """
        path = self._get_geotiff_path(parameter_id, month, year)

        if not path.exists():
            # For now, return None if file doesn't exist
            # In production, this will raise FileNotFoundError
            return None

        # TODO: Implement actual rasterio loading
        # return rasterio.open(path)
        return None

    def get_value_at_point(
        self,
        parameter_id: str,
        lat: float,
        lon: float,
        month: int,
        year: Optional[int] = None
    ) -> Optional[float]:
        """
        Get parameter value at a specific point.

        This is a mock implementation. Real implementation will:
        1. Load the GeoTIFF dataset
        2. Convert lat/lon to pixel coordinates
        3. Read and return the value at that pixel
        """
        # Mock data for testing
        # TODO: Replace with actual GeoTIFF reading logic
        mock_values = {
            "T2M": 25.0 + (lat / 10),  # Temperature
            "PRECTOTCORR": 50.0 + (lon / 10),  # Precipitation
            "CLOUD_AMT": 40.0,  # Cloud amount
            "RH2M": 60.0,  # Humidity
            "WS2M": 5.0,  # Wind speed
            "ALLSKY_SFC_SW_DWN": 6.0,  # Solar radiation
        }

        return mock_values.get(parameter_id)

    def get_values_in_radius(
        self,
        parameter_id: str,
        center_lat: float,
        center_lon: float,
        radius_km: float,
        month: int,
        resolution_km: float = 5.0,
        year: Optional[int] = None
    ) -> List[Tuple[float, float, float]]:
        """
        Get parameter values for all points within a radius.

        Returns:
            List of (lat, lon, value) tuples
        """
        from app.utils.geospatial import generate_grid_points

        # Generate grid of points
        grid_points = generate_grid_points(
            center_lat, center_lon, radius_km, resolution_km
        )

        results = []
        for lat, lon in grid_points:
            value = self.get_value_at_point(
                parameter_id, lat, lon, month, year
            )
            if value is not None:
                results.append((lat, lon, value))

        return results

    def get_monthly_values(
        self,
        parameter_id: str,
        lat: float,
        lon: float,
        year: Optional[int] = None
    ) -> Dict[int, float]:
        """Get parameter values for all 12 months at a location."""
        monthly_values = {}

        for month in range(1, 13):
            value = self.get_value_at_point(
                parameter_id, lat, lon, month, year
            )
            if value is not None:
                # Add some monthly variation for mock data
                seasonal_factor = np.sin((month - 1) * np.pi / 6) * 5
                monthly_values[month] = value + seasonal_factor

        return monthly_values

    def get_all_parameters(
        self,
        parameter_ids: List[str],
        lat: float,
        lon: float,
        month: int,
        year: Optional[int] = None
    ) -> Dict[str, float]:
        """Get values for multiple parameters at a point."""
        result = {}

        for param_id in parameter_ids:
            value = self.get_value_at_point(param_id, lat, lon, month, year)
            if value is not None:
                result[param_id] = value

        return result


# Global instance - will be initialized in main.py
data_service: DataService = None


def get_data_service() -> DataService:
    """Get the global data service instance."""
    if data_service is None:
        raise RuntimeError("Data service not initialized")
    return data_service
