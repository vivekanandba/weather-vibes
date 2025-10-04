import math
from typing import List, Tuple


def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).

    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point

    Returns:
        Distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers
    r = 6371

    return c * r


def generate_grid_points(
    center_lat: float,
    center_lon: float,
    radius_km: float,
    resolution_km: float
) -> List[Tuple[float, float]]:
    """
    Generate a grid of points within a radius.

    Args:
        center_lat: Center latitude
        center_lon: Center longitude
        radius_km: Search radius in kilometers
        resolution_km: Grid resolution in kilometers

    Returns:
        List of (lat, lon) tuples representing grid points
    """
    points = []

    # Convert km to approximate degrees
    # (rough approximation: 1 degree ≈ 111 km at equator)
    lat_deg_per_km = 1 / 111.0
    lon_deg_per_km = 1 / (111.0 * math.cos(math.radians(center_lat)))

    radius_lat = radius_km * lat_deg_per_km
    radius_lon = radius_km * lon_deg_per_km
    resolution_lat = resolution_km * lat_deg_per_km
    resolution_lon = resolution_km * lon_deg_per_km

    # Generate grid
    lat = center_lat - radius_lat
    while lat <= center_lat + radius_lat:
        lon = center_lon - radius_lon
        while lon <= center_lon + radius_lon:
            # Check if point is within radius
            distance = haversine_distance(center_lat, center_lon, lat, lon)
            if distance <= radius_km:
                points.append((lat, lon))
            lon += resolution_lon
        lat += resolution_lat

    return points


def lat_lon_to_pixel(
    lat: float,
    lon: float,
    geotransform: Tuple[float, ...]
) -> Tuple[int, int]:
    """
    Convert lat/lon to pixel coordinates using GeoTransform.

    GeoTransform format:
    (top_left_x, pixel_width, rotation_x, top_left_y, rotation_y, pixel_height)

    Args:
        lat: Latitude
        lon: Longitude
        geotransform: GDAL GeoTransform tuple

    Returns:
        Tuple of (row, col) pixel coordinates
    """
    origin_x = geotransform[0]
    pixel_width = geotransform[1]
    origin_y = geotransform[3]
    pixel_height = geotransform[5]

    # Calculate pixel coordinates
    col = int((lon - origin_x) / pixel_width)
    row = int((lat - origin_y) / pixel_height)

    return row, col
