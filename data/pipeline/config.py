"""Configuration models and helpers for the data extraction pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import yaml


@dataclass
class Parameter:
    """Represents a NASA POWER parameter to extract."""

    id: str
    aggregation: str
    description: str
    tags: List[str] = field(default_factory=list)


@dataclass
class PowerOptions:
    """Additional global options for API calls."""

    community: str
    temporal: str
    units: str
    max_year_span: int


@dataclass
class Area:
    """Area of interest definition."""

    name: str
    bounding_box: Optional[List[float]] = None
    description: Optional[str] = None
    center: Optional[List[float]] = None
    radius_km: Optional[float] = None


@dataclass
class PipelineConfig:
    """Root configuration for cron_job.py."""

    parameters: List[Parameter]
    options: PowerOptions
    areas: Dict[str, Area]

    @property
    def parameter_ids(self) -> List[str]:
        return [param.id for param in self.parameters]


def _load_yaml(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_pipeline_config(base_dir: Path) -> PipelineConfig:
    """Load YAML config files from ``base_dir``.

    Parameters
    ----------
    base_dir: Path
        Directory containing ``config`` subdirectory with parameter and area YAML files.
    """

    config_dir = base_dir / "config"
    params_data = _load_yaml(config_dir / "power_parameters.yml")
    areas_data = _load_yaml(config_dir / "areas_of_interest.yml")

    parameters = [Parameter(**entry) for entry in params_data["parameters"]]
    options = PowerOptions(**params_data["options"])

    areas = {
        key: Area(name=value.get("name", key),
                  bounding_box=value.get("bounding_box"),
                  description=value.get("description"),
                  center=value.get("center"),
                  radius_km=value.get("radius_km"))
        for key, value in areas_data.get("areas", {}).items()
    }

    return PipelineConfig(parameters=parameters, options=options, areas=areas)


def iter_year_chunks(start_year: int, end_year: int, span: int) -> Iterable[range]:
    """Yield consecutive year ranges honoring the max span constraint."""
    current = start_year
    while current <= end_year:
        chunk_end = min(current + span - 1, end_year)
        yield range(current, chunk_end + 1)
        current = chunk_end + 1
