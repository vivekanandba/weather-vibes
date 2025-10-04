"""Entry point for NASA POWER data extraction.

This script is intentionally lightweight: it wires together configuration loading,
request generation, fetching, and persistence. Business logic should live inside
``data/pipeline`` modules so the scheduler (Airflow/Cron) can import and reuse
components in tests.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from pipeline import (
    PipelineConfig,
    RawDataWriter,
    build_request_payload,
    fetch_chunk,
    iter_year_chunks,
    load_pipeline_config,
)

LOGGER = logging.getLogger("cron_job")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NASA POWER extraction job")
    parser.add_argument("start_year", type=int, help="First year to include (e.g., 2000)")
    parser.add_argument("end_year", type=int, help="Last year to include (inclusive)")
    parser.add_argument(
        "--area",
        default="south_india",
        help="Area of interest key from config/areas_of_interest.yml",
    )
    parser.add_argument(
        "--output-format",
        default="CSV",
        choices=["CSV", "JSON"],
        help="POWER API output format",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned requests without executing them",
    )
    parser.add_argument(
        "--base-dir",
        default=Path(__file__).resolve().parent,
        type=Path,
        help="Base directory containing config/ files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to store raw downloads (defaults to <base-dir>/outputs/raw)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    return parser.parse_args(argv)


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(name)s %(levelname)s - %(message)s",
    )


def run(
    config: PipelineConfig,
    *,
    base_dir: Path,
    output_dir: Path,
    area: str,
    start_year: int,
    end_year: int,
    output_format: str,
    dry_run: bool,
) -> None:
    if area not in config.areas:
        raise KeyError(f"Area '{area}' not found in config")

    writer = RawDataWriter(output_dir)
    max_span = config.options.max_year_span

    for years in iter_year_chunks(start_year, end_year, max_span):
        request = build_request_payload(
            config=config,
            area_key=area,
            years=list(years),
            output_format=output_format,
        )
        LOGGER.info("Prepared request for %s: %s", area, request.params)
        if dry_run:
            continue

        response = fetch_chunk(request)
        suffix = output_format.lower()
        year_label = f"{min(years)}-{max(years)}"
        writer.write(area=area, years=year_label, suffix=suffix, content=response.content)


if __name__ == "__main__":
    args = parse_args()
    configure_logging(args.log_level)

    base_dir = args.base_dir
    config = load_pipeline_config(base_dir)

    default_output_dir = (args.output_dir or (base_dir / "outputs")).resolve()

    run(
        config=config,
        base_dir=base_dir,
        output_dir=default_output_dir,
        area=args.area,
        start_year=args.start_year,
        end_year=args.end_year,
        output_format=args.output_format,
        dry_run=args.dry_run,
    )
