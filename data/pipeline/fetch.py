"""Helpers for building NASA POWER API requests."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

import requests

from .config import Area, PipelineConfig

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://power.larc.nasa.gov/api"


@dataclass
class FetchRequest:
    """Represents a single API call to the POWER service."""

    endpoint: str
    params: Mapping[str, str]
    area_key: str
    years: Sequence[int]


def build_request_payload(
    config: PipelineConfig,
    area_key: str,
    years: Sequence[int],
    temporal: Optional[str] = None,
    output_format: str = "CSV",
) -> FetchRequest:
    """Construct the API request parameters for a chunk of years."""
    area = config.areas[area_key]
    temporal = temporal or config.options.temporal

    base_params = {
        "community": config.options.community,
        "parameters": ",".join(config.parameter_ids),
        "start": f"{min(years)}0101",
        "end": f"{max(years)}1231",
        "format": output_format,
        "units": config.options.units,
    }

    if area.bounding_box:
        endpoint = f"{BASE_URL}/temporal/{temporal}/region"
        base_params["boundingBox"] = ",".join(str(value) for value in area.bounding_box)
    else:
        endpoint = f"{BASE_URL}/temporal/{temporal}/point"
        if not area.center:
            raise ValueError(f"Center is required for point extraction: {area_key}")
        lat, lon = area.center
        base_params["latitude"] = str(lat)
        base_params["longitude"] = str(lon)

    return FetchRequest(endpoint=endpoint, params=base_params, area_key=area_key, years=years)


def fetch_chunk(request: FetchRequest, session: Optional[requests.Session] = None) -> requests.Response:
    """Execute the HTTP request and return the response object.

    Caller is responsible for checking status and writing to disk.
    """
    sess = session or requests.Session()
    LOGGER.info("Fetching %s for %s (%s)", request.endpoint, request.area_key, request.years)
    response = sess.get(request.endpoint, params=request.params, timeout=60)
    response.raise_for_status()
    return response
