"""Aggregation utilities for NASA POWER point downloads."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, MutableMapping

import numpy as np
import pandas as pd

from .config import Parameter

LOGGER = logging.getLogger(__name__)

FILL_VALUE = -999.0
DATE_FORMAT = "%Y%m%d"


@dataclass
class MonthlyAggregationResult:
    """Holds the aggregated dataframe and any metadata."""

    area: str
    source_file: Path
    dataframe: pd.DataFrame


# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------


def load_point_json(path: Path) -> pd.DataFrame:
    """Load a POWER point JSON dump into a daily-resolution DataFrame."""
    LOGGER.debug("Loading point JSON: %s", path)
    payload = json.loads(path.read_text())
    parameters: Mapping[str, Mapping[str, float]] = payload["properties"]["parameter"]

    all_dates = sorted({date for series in parameters.values() for date in series.keys()})
    data: MutableMapping[str, list] = {"date": [pd.to_datetime(date, format=DATE_FORMAT) for date in all_dates]}

    for param_id, series in parameters.items():
        values = [series.get(date, np.nan) for date in all_dates]
        data[param_id] = values

    df = pd.DataFrame(data).set_index("date").sort_index()
    df.replace(FILL_VALUE, np.nan, inplace=True)
    numeric_cols = [col for col in df.columns if col != "date"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df


# ---------------------------------------------------------------------------
# Aggregation logic
# ---------------------------------------------------------------------------


def _build_agg_spec(parameters: Iterable[Parameter]) -> Mapping[str, str]:
    spec: dict[str, str] = {}
    for param in parameters:
        agg = param.aggregation.lower()
        if agg in {"mean", "avg"}:
            spec[param.id] = "mean"
        elif agg in {"sum", "total"}:
            spec[param.id] = "sum"
        elif agg in {"min", "minimum"}:
            spec[param.id] = "min"
        elif agg in {"max", "maximum"}:
            spec[param.id] = "max"
        else:
            LOGGER.warning("Unknown aggregation '%s' for %s, defaulting to mean", param.aggregation, param.id)
            spec[param.id] = "mean"
    return spec


def _compute_mild_score(series: pd.Series, optimal_min: float = 18.0, optimal_max: float = 25.0) -> pd.Series:
    """Return a 0-100 score where values inside [optimal_min, optimal_max] score best."""
    midpoint = (optimal_min + optimal_max) / 2.0
    width = (optimal_max - optimal_min) / 2.0
    diff = (series - midpoint).abs()
    score = 1 - (diff / (width if width else 1.0))
    return (score.clip(lower=0, upper=1) * 100).round(2)


def _compute_stargazing_score(cloud_fraction: pd.Series, rh_series: pd.Series) -> pd.Series:
    if cloud_fraction is None or rh_series is None:
        return pd.Series(dtype=float)
    clarity = (1 - cloud_fraction.clip(0, 1)) * (1 - (rh_series.clip(0, 100) / 100.0))
    return (clarity.clip(lower=0) * 100).round(2)


def compute_monthly_statistics(
    *,
    daily_df: pd.DataFrame,
    parameters: Iterable[Parameter],
    include_derived: bool = True,
) -> pd.DataFrame:
    """Aggregate daily data into monthly statistics and optional derived scores."""
    if daily_df.empty:
        raise ValueError("Daily dataframe is empty; cannot aggregate")

    agg_spec = _build_agg_spec(parameters)
    monthly = daily_df.resample("MS").agg(agg_spec)

    # Derived metrics
    if include_derived:
        if {"ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN"}.issubset(monthly.columns):
            ratio = monthly["ALLSKY_SFC_SW_DWN"] / monthly["CLRSKY_SFC_SW_DWN"].replace(0, np.nan)
            cloud_fraction = 1 - ratio
            monthly["CLOUD_FRACTION"] = cloud_fraction.clip(0, 1)
        else:
            monthly["CLOUD_FRACTION"] = np.nan

        if "PRECTOTCORR" in daily_df.columns:
            rain_days = (daily_df["PRECTOTCORR"] >= 1.0).resample("MS").sum()
            total_days = daily_df["PRECTOTCORR"].resample("MS").count()
            monthly["RAINY_DAY_COUNT"] = rain_days
            monthly["RAINY_DAY_FRACTION"] = (rain_days / total_days).round(4)

        if "T2M" in monthly.columns:
            monthly["MILD_SCORE"] = _compute_mild_score(monthly["T2M"])

        if "RH2M" in monthly.columns:
            monthly["STARGAZING_SCORE"] = _compute_stargazing_score(
                monthly.get("CLOUD_FRACTION"), monthly["RH2M"]
            )

    monthly.index.name = "month"
    return monthly.reset_index()


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def export_monthly_to_csv(df: pd.DataFrame, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    LOGGER.info("Wrote monthly summary: %s", destination)
    return destination


def export_monthly_to_parquet(df: pd.DataFrame, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(destination, index=False)
    except ImportError:  # pyarrow / fastparquet missing
        LOGGER.warning("Parquet dependencies missing; skipping %s", destination)
        return destination
    LOGGER.info("Wrote monthly summary: %s", destination)
    return destination


def aggregate_point_file(
    *,
    path: Path,
    area: str,
    parameters: Iterable[Parameter],
    output_dir: Path,
) -> MonthlyAggregationResult:
    daily_df = load_point_json(path)
    monthly_df = compute_monthly_statistics(daily_df=daily_df, parameters=parameters)

    csv_path = output_dir / "csv" / f"{area}__{path.stem}.csv"
    parquet_path = output_dir / "parquet" / f"{area}__{path.stem}.parquet"
    export_monthly_to_csv(monthly_df, csv_path)
    export_monthly_to_parquet(monthly_df, parquet_path)

    return MonthlyAggregationResult(area=area, source_file=path, dataframe=monthly_df)
