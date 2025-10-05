from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
import numpy as np
from functools import lru_cache
from datetime import datetime


class DataService:
    """Service for accessing NASA POWER climate data from JSON files."""

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.cache: Dict = {}
        self.locations_cache: Dict[str, Dict] = {}
        self._load_available_locations()

    def _load_available_locations(self):
        """Load metadata about available point locations."""
        try:
            # Check if we have the outputs directory
            outputs_dir = self.data_path / "outputs"
            if not outputs_dir.exists():
                print(f"Warning: Data outputs directory not found at {outputs_dir}")
                return

            # Find all point directories
            for location_dir in outputs_dir.iterdir():
                if location_dir.is_dir() and location_dir.name.endswith("_point"):
                    location_name = location_dir.name.replace("_point", "")

                    # Check for raw data files
                    raw_dir = location_dir / "raw"
                    if raw_dir.exists():
                        json_files = list(raw_dir.glob("*.json"))
                        if json_files:
                            # Load the first file to get coordinates
                            with open(json_files[0], 'r') as f:
                                data = json.load(f)
                                coords = data["geometry"]["coordinates"]
                                self.locations_cache[location_name] = {
                                    "lat": coords[1],
                                    "lon": coords[0],
                                    "files": json_files,
                                    "raw_dir": raw_dir
                                }

            print(f"Loaded {len(self.locations_cache)} point locations")
        except Exception as e:
            print(f"Error loading locations: {e}")

    def _find_nearest_location(self, lat: float, lon: float) -> Optional[str]:
        """Find the nearest available location to the given coordinates."""
        if not self.locations_cache:
            return None

        min_distance = float('inf')
        nearest_location = None

        for location_name, location_data in self.locations_cache.items():
            # Simple distance calculation (not perfect for large distances)
            distance = np.sqrt(
                (lat - location_data["lat"]) ** 2 +
                (lon - location_data["lon"]) ** 2
            )

            if distance < min_distance:
                min_distance = distance
                nearest_location = location_name

        return nearest_location

    def _load_location_data(self, location_name: str) -> Optional[Dict]:
        """Load all data for a location from JSON files."""
        if location_name not in self.locations_cache:
            return None

        # Check cache first
        cache_key = f"location_{location_name}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        location_data = self.locations_cache[location_name]
        all_data = {"parameters": {}}

        try:
            # Load all JSON files for this location
            for json_file in location_data["files"]:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    parameters = data["properties"]["parameter"]

                    # Merge parameter data
                    for param_name, param_values in parameters.items():
                        if param_name not in all_data["parameters"]:
                            all_data["parameters"][param_name] = {}
                        all_data["parameters"][param_name].update(param_values)

            # Store coordinates
            all_data["lat"] = location_data["lat"]
            all_data["lon"] = location_data["lon"]

            # Cache the loaded data
            self.cache[cache_key] = all_data
            return all_data

        except Exception as e:
            print(f"Error loading data for {location_name}: {e}")
            return None

    def _aggregate_monthly(
        self,
        daily_data: Dict[str, float],
        month: int,
        year: Optional[int] = None
    ) -> Optional[float]:
        """
        Aggregate daily data to monthly average.

        Args:
            daily_data: Dictionary mapping date strings (YYYYMMDD) to values
            month: Month number (1-12)
            year: Optional year filter

        Returns:
            Monthly average value or None if no data
        """
        values = []

        for date_str, value in daily_data.items():
            try:
                date_obj = datetime.strptime(date_str, "%Y%m%d")

                # Filter by month and optionally year
                if date_obj.month == month:
                    if year is None or date_obj.year == year:
                        values.append(value)
            except:
                continue

        if not values:
            return None

        return np.mean(values)

    def get_value_at_point(
        self,
        parameter_id: str,
        lat: float,
        lon: float,
        month: int,
        year: Optional[int] = None
    ) -> Optional[float]:
        """
        Get parameter value at a specific point, aggregated monthly.

        Args:
            parameter_id: NASA POWER parameter ID (e.g., "T2M", "PRECTOTCORR")
            lat: Latitude
            lon: Longitude
            month: Month number (1-12)
            year: Optional year (if None, uses all available years)

        Returns:
            Monthly average value or None if no data available
        """
        # Find nearest location
        location_name = self._find_nearest_location(lat, lon)
        if not location_name:
            print(f"No location data found near {lat}, {lon}")
            return None

        # Load location data
        location_data = self._load_location_data(location_name)
        if not location_data:
            return None

        # Get parameter data
        if parameter_id not in location_data["parameters"]:
            print(f"Parameter {parameter_id} not available for {location_name}")
            return None

        daily_data = location_data["parameters"][parameter_id]

        # Aggregate to monthly
        return self._aggregate_monthly(daily_data, month, year)

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

        Since we only have point data, this returns values for all available
        locations within the radius.

        Returns:
            List of (lat, lon, value) tuples
        """
        results = []

        # Convert km to approximate degrees (rough approximation)
        radius_deg = radius_km / 111.0  # 1 degree ≈ 111 km

        for location_name, location_info in self.locations_cache.items():
            loc_lat = location_info["lat"]
            loc_lon = location_info["lon"]

            # Check if within radius
            distance = np.sqrt(
                (center_lat - loc_lat) ** 2 +
                (center_lon - loc_lon) ** 2
            )

            if distance <= radius_deg:
                value = self.get_value_at_point(
                    parameter_id, loc_lat, loc_lon, month, year
                )
                if value is not None:
                    results.append((loc_lat, loc_lon, value))

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
                monthly_values[month] = value

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

    def get_available_locations(self) -> List[Dict[str, any]]:
        """Get list of all available locations."""
        return [
            {
                "name": name,
                "lat": info["lat"],
                "lon": info["lon"]
            }
            for name, info in self.locations_cache.items()
        ]


# Global instance - will be initialized in main.py
data_service: DataService = None


def get_data_service() -> DataService:
    """Get the global data service instance."""
    if data_service is None:
        raise RuntimeError("Data service not initialized")
    return data_service
