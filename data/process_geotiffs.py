#!/usr/bin/env python3
"""
GeoTIFF Processing Script for Weather Vibes

This script processes the monthly aggregated CSV data into GeoTIFF files
that can be used by the FastAPI backend for vibe scoring.

Usage:
    python process_geotiffs.py --input-dir outputs --output-dir geotiffs
"""

import argparse
import logging
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.crs import CRS
import geopandas as gpd
from shapely.geometry import Point
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s - %(message)s'
)
logger = logging.getLogger("geotiff_processor")


class GeoTIFFProcessor:
    """Processes monthly CSV data into GeoTIFF files for vibe scoring."""
    
    def __init__(self, input_dir: Path, output_dir: Path, config_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.config_dir = config_dir
        
        # Load configuration
        self.areas_config = self._load_areas_config()
        self.parameters_config = self._load_parameters_config()
        self.vibe_config = self._load_vibe_config()
        
        # Create output directory structure
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_areas_config(self) -> Dict:
        """Load areas of interest configuration."""
        with open(self.config_dir / "areas_of_interest.yml") as f:
            return yaml.safe_load(f)
    
    def _load_parameters_config(self) -> Dict:
        """Load parameters configuration."""
        with open(self.config_dir / "power_parameters.yml") as f:
            return yaml.safe_load(f)
    
    def _load_vibe_config(self) -> Dict:
        """Load vibe dictionary configuration."""
        with open(Path(__file__).parent.parent / "server" / "config" / "vibe_dictionary.json") as f:
            return json.load(f)
    
    def process_all_areas(self) -> None:
        """Process all areas and create GeoTIFF files."""
        logger.info("Starting GeoTIFF processing for all areas...")
        
        for area_key, area_info in self.areas_config["areas"].items():
            if "center" in area_info:  # Point data
                self.process_point_area(area_key, area_info)
            else:  # Regional data
                self.process_regional_area(area_key, area_info)
        
        logger.info("GeoTIFF processing completed!")
    
    def process_point_area(self, area_key: str, area_info: Dict) -> None:
        """Process point-based area data into GeoTIFF files."""
        logger.info(f"Processing point area: {area_key}")
        
        # Load monthly data
        csv_path = self.input_dir / area_key / "monthly" / f"{area_key}__monthly_summary.csv"
        if not csv_path.exists():
            logger.warning(f"CSV file not found: {csv_path}")
            return
        
        df = pd.read_csv(csv_path)
        df['date'] = pd.to_datetime(df['month'])
        df['month'] = df['date'].dt.month
        
        # Get center coordinates
        lat, lon = area_info["center"]
        
        # Process each vibe
        for vibe_id, vibe_config in self.vibe_config.items():
            if vibe_config.get("type") == "advisor":
                continue  # Skip advisor vibes for now
                
            self.process_vibe_for_point(vibe_id, vibe_config, df, lat, lon)
    
    def process_vibe_for_point(self, vibe_id: str, vibe_config: Dict, df: pd.DataFrame, lat: float, lon: float) -> None:
        """Process a specific vibe for point data."""
        logger.info(f"Processing vibe {vibe_id} for point data")
        
        # Create vibe output directory
        vibe_dir = self.output_dir / vibe_id
        vibe_dir.mkdir(exist_ok=True)
        
        # Process each parameter
        for param_config in vibe_config.get("parameters", []):
            param_id = param_config["id"]
            
            # Create parameter directory
            param_dir = vibe_dir / param_id
            param_dir.mkdir(exist_ok=True)
            
            # Process each month
            for month in range(1, 13):
                month_data = df[df['month'] == month]
                if month_data.empty:
                    continue
                
                # Get the value for this parameter and month
                if param_id in month_data.columns:
                    value = month_data[param_id].iloc[0]
                else:
                    logger.warning(f"Parameter {param_id} not found in data for month {month}")
                    continue
                
                # Create GeoTIFF for this parameter and month
                self.create_point_geotiff(
                    param_dir / f"month_{month:02d}.tif",
                    value, lat, lon, param_id, month
                )
    
    def create_point_geotiff(self, output_path: Path, value: float, lat: float, lon: float, 
                           param_id: str, month: int) -> None:
        """Create a GeoTIFF file for a single point value."""
        
        # Create a small grid around the point (0.1 degree resolution)
        resolution = 0.1
        grid_size = 3  # 3x3 grid
        
        # Calculate bounds
        half_res = resolution / 2
        west = lon - half_res
        east = lon + half_res
        north = lat + half_res
        south = lat - half_res
        
        # Create grid
        lons = np.linspace(west, east, grid_size)
        lats = np.linspace(north, south, grid_size)
        
        # Create data array (all values are the same for point data)
        data = np.full((grid_size, grid_size), value, dtype=np.float32)
        
        # Create transform
        transform = from_bounds(west, south, east, north, grid_size, grid_size)
        
        # Write GeoTIFF
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=grid_size,
            width=grid_size,
            count=1,
            dtype=data.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform,
            compress='lzw'
        ) as dst:
            dst.write(data, 1)
            
            # Add metadata
            dst.update_tags(
                parameter=param_id,
                month=month,
                value=value,
                location_lat=lat,
                location_lon=lon,
                data_source="NASA POWER API",
                processing_date=pd.Timestamp.now().isoformat()
            )
        
        logger.debug(f"Created GeoTIFF: {output_path}")
    
    def process_regional_area(self, area_key: str, area_info: Dict) -> None:
        """Process regional area data into GeoTIFF files."""
        logger.info(f"Processing regional area: {area_key}")
        
        # For regional data, we would need to interpolate between points
        # This is a more complex operation that would require spatial interpolation
        # For now, we'll skip regional processing and focus on point data
        logger.warning(f"Regional processing not implemented for {area_key}")
    
    def create_cloud_fraction_geotiffs(self) -> None:
        """Create cloud fraction GeoTIFFs from ALLSKY and CLRSKY data."""
        logger.info("Creating cloud fraction GeoTIFFs...")
        
        for area_key, area_info in self.areas_config["areas"].items():
            if "center" not in area_info:
                continue
                
            # Load monthly data
            csv_path = self.input_dir / area_key / "monthly" / f"{area_key}__monthly_summary.csv"
            if not csv_path.exists():
                continue
            
            df = pd.read_csv(csv_path)
            df['date'] = pd.to_datetime(df['month'])
            df['month'] = df['date'].dt.month
            
            # Calculate cloud fraction if not already present
            if 'CLOUD_FRACTION' not in df.columns and 'ALLSKY_SFC_SW_DWN' in df.columns and 'CLRSKY_SFC_SW_DWN' in df.columns:
                df['CLOUD_FRACTION'] = 1 - (df['ALLSKY_SFC_SW_DWN'] / df['CLRSKY_SFC_SW_DWN'])
                df['CLOUD_FRACTION'] = df['CLOUD_FRACTION'].clip(0, 1)  # Clamp to [0,1]
            
            # Create CLOUD_AMT parameter (same as CLOUD_FRACTION for stargazing)
            df['CLOUD_AMT'] = df['CLOUD_FRACTION'] * 100  # Convert to percentage
            
            # Process stargazing vibe with cloud data
            lat, lon = area_info["center"]
            self.process_vibe_for_point("stargazing", self.vibe_config["stargazing"], df, lat, lon)


def main():
    parser = argparse.ArgumentParser(description="Process monthly CSV data into GeoTIFF files")
    parser.add_argument("--input-dir", type=Path, default=Path("outputs"),
                       help="Input directory containing monthly CSV files")
    parser.add_argument("--output-dir", type=Path, default=Path("geotiffs"),
                       help="Output directory for GeoTIFF files")
    parser.add_argument("--config-dir", type=Path, default=Path("config"),
                       help="Configuration directory")
    parser.add_argument("--log-level", default="INFO",
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Configure logging
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    # Process GeoTIFFs
    processor = GeoTIFFProcessor(args.input_dir, args.output_dir, args.config_dir)
    processor.process_all_areas()
    processor.create_cloud_fraction_geotiffs()


if __name__ == "__main__":
    main()
