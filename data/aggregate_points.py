"""Aggregate downloaded POWER point data into monthly summaries."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable

import pandas as pd

from pipeline import (
    PipelineConfig,
    aggregate_point_file,
    load_pipeline_config,
)

LOGGER = logging.getLogger("aggregate_points")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate POWER point downloads")
    parser.add_argument(
        "--base-dir",
        default=Path(__file__).resolve().parent,
        type=Path,
        help="Base directory containing config/ and outputs/",
    )
    parser.add_argument(
        "--areas",
        nargs="*",
        help="Subset of area keys to process (defaults to all point-defined areas)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level",
    )
    return parser.parse_args()


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(name)s %(levelname)s - %(message)s",
    )


def _iter_point_areas(config: PipelineConfig) -> Iterable[str]:
    for key, area in config.areas.items():
        if area.bounding_box:
            continue
        yield key


def aggregate_area(*, config: PipelineConfig, base_dir: Path, area_key: str) -> Path | None:
    parameters = config.parameters
    raw_dir = base_dir / "outputs" / area_key / "raw"
    if not raw_dir.exists():
        LOGGER.warning("No raw data found for %s", area_key)
        return None

    monthly_outputs = base_dir / "outputs" / area_key / "monthly"
    combined_frames: list[pd.DataFrame] = []

    for path in sorted(raw_dir.glob("*.json")):
        result = aggregate_point_file(
            path=path,
            area=area_key,
            parameters=parameters,
            output_dir=monthly_outputs,
        )
        combined_frames.append(result.dataframe)

    if not combined_frames:
        LOGGER.warning("No JSON files processed for %s", area_key)
        return None

    combined = pd.concat(combined_frames, ignore_index=True).sort_values("month")
    combined_path = monthly_outputs / f"{area_key}__monthly_summary.parquet"
    combined_csv = monthly_outputs / f"{area_key}__monthly_summary.csv"
    try:
        combined.to_parquet(combined_path, index=False)
        parquet_written = True
    except ImportError:
        LOGGER.warning("Parquet dependencies missing; skipping %s", combined_path)
        parquet_written = False
    combined.to_csv(combined_csv, index=False)
    LOGGER.info("Wrote combined CSV summary: %s", combined_csv)
    return combined_path if parquet_written else combined_csv


def main() -> None:
    args = parse_args()
    configure_logging(args.log_level)

    base_dir = args.base_dir
    config = load_pipeline_config(base_dir)

    target_areas = args.areas or list(_iter_point_areas(config))
    LOGGER.info("Aggregating areas: %s", target_areas)

    for area in target_areas:
        aggregate_area(config=config, base_dir=base_dir, area_key=area)


if __name__ == "__main__":
    main()
