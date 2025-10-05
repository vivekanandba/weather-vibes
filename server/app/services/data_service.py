from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
import numpy as np
from functools import lru_cache
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)


class DataService:
    """Service for accessing NASA POWER climate data from JSON files."""

    def __init__(self, data_path: str):
        logger.info(f"Initializing DataService with path: {data_path}")
        self.data_path = Path(data_path)
        self.cache: Dict = {}
        self.locations_cache: Dict[str, Dict] = {}
        self._load_available_locations()
        logger.info(
            f"DataService initialized with {len(self.locations_cache)} locations"
        )

    def _load_available_locations(self):
        """Load metadata about available point locations."""
        logger.info("Loading available locations")
        try:
            # Check if we have the outputs directory
            outputs_dir = self.data_path / "outputs"
            if not outputs_dir.exists():
                logger.warning(f"Data outputs directory not found at {outputs_dir}")
                return

            # Find all point directories
            for location_dir in outputs_dir.iterdir():
                if location_dir.is_dir() and location_dir.name.endswith("_point"):
                    location_name = location_dir.name.replace("_point", "")
                    logger.debug(f"Processing location: {location_name}")

                    # Check for raw data files
                    raw_dir = location_dir / "raw"
                    if raw_dir.exists():
                        json_files = list(raw_dir.glob("*.json"))
                        if json_files:
                            logger.debug(
                                f"Found {len(json_files)} JSON files for {location_name}"
                            )
                            # Load the first file to get coordinates
                            with open(json_files[0], "r") as f:
                                data = json.load(f)
                                coords = data["geometry"]["coordinates"]
                                self.locations_cache[location_name] = {
                                    "lat": coords[1],
                                    "lon": coords[0],
                                    "files": json_files,
                                    "raw_dir": raw_dir,
                                }
                        else:
                            logger.warning(f"No JSON files found for {location_name}")
                    else:
                        logger.warning(f"No raw directory found for {location_name}")

            logger.info(f"Loaded {len(self.locations_cache)} point locations")
        except Exception as e:
            logger.error(f"Error loading locations: {e}")

    def _find_nearest_location(self, lat: float, lon: float) -> Optional[str]:
        """Find the nearest available location to the given coordinates."""
        logger.debug(f"Finding nearest location for ({lat}, {lon})")

        if not self.locations_cache:
            logger.warning("No locations available in cache")
            return None

        min_distance = float("inf")
        nearest_location = None

        for location_name, location_data in self.locations_cache.items():
            # Simple distance calculation (not perfect for large distances)
            distance = np.sqrt(
                (lat - location_data["lat"]) ** 2 + (lon - location_data["lon"]) ** 2
            )

            if distance < min_distance:
                min_distance = distance
                nearest_location = location_name

        logger.debug(
            f"Nearest location: {nearest_location} (distance: {min_distance:.4f})"
        )
        return nearest_location

    def _load_location_data(self, location_name: str) -> Optional[Dict]:
        """Load all data for a location from JSON files."""
        logger.debug(f"Loading data for location: {location_name}")

        if location_name not in self.locations_cache:
            logger.error(f"Location {location_name} not found in cache")
            return None

        # Check cache first
        cache_key = f"location_{location_name}"
        if cache_key in self.cache:
            logger.debug(f"Using cached data for {location_name}")
            return self.cache[cache_key]

        location_data = self.locations_cache[location_name]
        all_data = {"parameters": {}}

        try:
            logger.debug(
                f"Loading {len(location_data['files'])} files for {location_name}"
            )
            # Load all JSON files for this location
            for json_file in location_data["files"]:
                logger.debug(f"Loading file: {json_file.name}")
                with open(json_file, "r") as f:
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
            logger.info(
                f"Loaded data for {location_name} with {len(all_data['parameters'])} parameters"
            )
            return all_data

        except Exception as e:
            logger.error(f"Error loading data for {location_name}: {e}")
            return None

    def _aggregate_monthly(
        self,
        daily_data: Dict[str, float],
        month: int,
        year: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
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

                # Filter by month first
                if date_obj.month != month:
                    continue

                # Optional year filter
                if year is not None and date_obj.year != year:
                    continue

                # Optional date range clamp (intersect month with range when provided)
                if start_date and date_obj < start_date:
                    continue
                if end_date and date_obj > end_date:
                    continue

                values.append(value)
            except:
                continue

        if not values:
            return None

        return np.mean(values)

    def _aggregate_date_range(
        self,
        daily_data: Dict[str, float],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Optional[float]:
        """
        Aggregate daily data to date range average.

        Args:
            daily_data: Dictionary mapping date strings (YYYYMMDD) to values
            start_date: Start date for filtering
            end_date: End date for filtering

        Returns:
            Date range average value or None if no data
        """
        values = []

        for date_str, value in daily_data.items():
            try:
                date_obj = datetime.strptime(date_str, "%Y%m%d")

                # Filter by date range if provided
                if start_date and end_date:
                    if start_date <= date_obj <= end_date:
                        values.append(value)
                elif start_date:
                    if date_obj >= start_date:
                        values.append(value)
                elif end_date:
                    if date_obj <= end_date:
                        values.append(value)
                else:
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
        month: Optional[int] = None,
        year: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Optional[float]:
        """
        Get parameter value at a specific point, aggregated monthly or by date range.

        Args:
            parameter_id: NASA POWER parameter ID (e.g., "T2M", "PRECTOTCORR")
            lat: Latitude
            lon: Longitude
            month: Month number (1-12) - optional if using date range
            year: Optional year (if None, uses all available years)
            start_date: Start date for date range filtering
            end_date: End date for date range filtering

        Returns:
            Aggregated value or None if no data available
        """
        logger.debug(
            f"Getting value for {parameter_id} at ({lat}, {lon}), month={month}, year={year}, start_date={start_date}, end_date={end_date}"
        )

        # Find nearest location
        location_name = self._find_nearest_location(lat, lon)
        if not location_name:
            logger.warning(f"No location data found near {lat}, {lon}")
            return None

        # Load location data
        location_data = self._load_location_data(location_name)
        if not location_data:
            logger.error(f"Failed to load data for {location_name}")
            return None

        # Get parameter data
        if parameter_id not in location_data["parameters"]:
            logger.warning(
                f"Parameter {parameter_id} not available for {location_name}"
            )
            return None

        daily_data = location_data["parameters"][parameter_id]
        logger.debug(f"Found {len(daily_data)} daily data points for {parameter_id}")

        # Compute available data range
        try:
            all_dates = [datetime.strptime(k, "%Y%m%d") for k in daily_data.keys()]
            min_date = min(all_dates)
            max_date = max(all_dates)
        except Exception as e:
            logger.warning(f"Failed parsing date keys for {parameter_id}: {e}")
            min_date = None
            max_date = None

        # Prefer monthly aggregation when month is specified
        if month is not None:
            # If a specific year was requested but is outside available data, ignore year filter
            effective_year = year
            if min_date and max_date and year is not None:
                if year < min_date.year or year > max_date.year:
                    logger.info(
                        f"Year {year} out of available range {min_date.year}-{max_date.year}. Falling back to all years."
                    )
                    effective_year = None

            logger.debug(
                f"Using monthly aggregation for month {month}, year={effective_year}"
            )
            result = self._aggregate_monthly(daily_data, month, effective_year)

        elif start_date or end_date:
            # Clamp requested range to available data
            clamped_start = start_date
            clamped_end = end_date
            if min_date:
                if clamped_start and clamped_start < min_date:
                    clamped_start = min_date
                if clamped_end and clamped_end < min_date:
                    clamped_end = min_date
            if max_date:
                if clamped_start and clamped_start > max_date:
                    clamped_start = max_date
                if clamped_end and clamped_end > max_date:
                    clamped_end = max_date

            # If clamped range is invalid, fall back to overall average
            if clamped_start and clamped_end and clamped_start > clamped_end:
                logger.info(
                    f"Requested date range has no overlap with data ({start_date}..{end_date} vs {min_date}..{max_date}). Returning overall average."
                )
                values = list(daily_data.values())
                result = np.mean(values) if values else None
            else:
                logger.debug(
                    f"Using date range aggregation: start={clamped_start}, end={clamped_end}"
                )
                result = self._aggregate_date_range(
                    daily_data, clamped_start, clamped_end
                )

        else:
            logger.debug("Using overall average aggregation")
            # If no specific time filter, return overall average
            values = list(daily_data.values())
            result = np.mean(values) if values else None

        logger.debug(f"Final aggregated value: {result}")
        return result

    def get_values_in_radius(
        self,
        parameter_id: str,
        center_lat: float,
        center_lon: float,
        radius_km: float,
        month: Optional[int] = None,
        resolution_km: float = 5.0,
        year: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
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
                (center_lat - loc_lat) ** 2 + (center_lon - loc_lon) ** 2
            )

            if distance <= radius_deg:
                value = self.get_value_at_point(
                    parameter_id, loc_lat, loc_lon, month, year, start_date, end_date
                )
                if value is not None:
                    results.append((loc_lat, loc_lon, value))

        return results

    def get_monthly_values(
        self, parameter_id: str, lat: float, lon: float, year: Optional[int] = None
    ) -> Dict[int, float]:
        """Get parameter values for all 12 months at a location."""
        monthly_values = {}

        for month in range(1, 13):
            value = self.get_value_at_point(parameter_id, lat, lon, month, year)
            if value is not None:
                monthly_values[month] = value

        return monthly_values

    def get_all_parameters(
        self,
        parameter_ids: List[str],
        lat: float,
        lon: float,
        month: Optional[int] = None,
        year: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, float]:
        """Get values for multiple parameters at a point."""
        logger.debug(
            f"Getting all parameters {parameter_ids} at ({lat}, {lon}), month={month}, year={year}"
        )

        result = {}

        for param_id in parameter_ids:
            logger.debug(f"Getting parameter: {param_id}")
            value = self.get_value_at_point(
                param_id, lat, lon, month, year, start_date, end_date
            )
            if value is not None:
                result[param_id] = value
                logger.debug(f"Got value for {param_id}: {value}")
            else:
                logger.warning(f"No value found for {param_id}")

        logger.debug(f"Final result: {result}")
        return result

    def get_available_locations(self) -> List[Dict[str, any]]:
        """Get list of all available locations."""
        return [
            {"name": name, "lat": info["lat"], "lon": info["lon"]}
            for name, info in self.locations_cache.items()
        ]


# Global instance - will be initialized in main.py
data_service: DataService = None


def get_data_service() -> DataService:
    """Get the global data service instance."""
    if data_service is None:
        raise RuntimeError("Data service not initialized")
    return data_service
