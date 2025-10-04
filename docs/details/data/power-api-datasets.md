# NASA POWER API: Data Sourcing Plan

This document outlines the datasets, API usage patterns, and processing plan to acquire and prepare NASA POWER data for Weather Vibes.

## Purpose
- Define the exact POWER parameters needed to support the "Where" and "When" features and the "Advisors".
- Provide reliable query templates (point and region) for batch acquisition.
- Describe aggregation/derivation steps and storage conventions for GeoTIFFs.

## Required Parameters (Daily)
- Temperature: `T2M`, `T2M_MIN`, `T2M_MAX` — mild climate bands, comfort indices.
- Humidity: `RH2M` — clarity/mist scoring, comfort.
- Precipitation: `PRECTOTCORR` — rain probability, rainy-day detection.
- Wind: `WS2M` — comfort, stylist advisor.
- Solar irradiance: `ALLSKY_SFC_SW_DWN` — sunny/clear conditions, beach day.
- Cloudiness: Prefer direct cloud cover if available; otherwise derive cloud fraction using `ALLSKY_SFC_SW_DWN` vs `CLRSKY_SFC_SW_DWN`.

Optional (useful)
- Dew point: `T2MDEW` — fog/mist detection and comfort.
- Clear-sky irradiance: `CLRSKY_SFC_SW_DWN` — to estimate cloud fraction when cloud amount is not directly exposed.

Notes
- The project’s vibe dictionary references: `CLOUD_AMT`, `RH2M`, `ALLSKY_SFC_SW_DWN`, `T2M`, `PRECTOTCORR`, `WS2M`.
- If `CLOUD_AMT` isn’t directly available in POWER for a chosen community/temporal mode, estimate cloud fraction as: `1 - (ALLSKY / CLRSKY)` (clamped to [0,1]).

## Temporal and Spatial Scope
- Temporal: daily time series (1981–present) to compute monthly climatology, percentiles, and event probabilities.
- Spatial: POWER native 0.5° grid over the areas of interest (e.g., South India; expand as needed).
- Output: precomputed monthly layers (means or totals) for fast heatmaps and calendars.

## API Query Patterns
Base: https://power.larc.nasa.gov/docs/services/api/

Common query options
- `temporal`: `hourly`, `daily`, `monthly`, `climatology` (we primarily use `daily`, plus `monthly` and `climatology` summaries).
- `community`: typically `ag` (agriculture) for the above parameters; others include `re`, `sb`.
- `format`: `JSON` or `CSV` (CSV recommended for batch ingestion).
- `start`, `end`: `YYYYMMDD` for `daily`; `YYYYMM` for `monthly`.
- `units`: `metric` or `imperial` (use `metric`).

Examples

1) Daily point (prototype/testing)
```
https://power.larc.nasa.gov/api/temporal/daily/point?
  community=ag&
  parameters=T2M,T2M_MIN,T2M_MAX,RH2M,PRECTOTCORR,WS2M,ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN&
  start=20000101&end=20241231&
  latitude=12.97&longitude=77.59&
  format=JSON&units=metric
```

2) Daily region (batch over a bounding box)
```
https://power.larc.nasa.gov/api/temporal/daily/region?
  community=ag&
  parameters=T2M,RH2M,PRECTOTCORR,WS2M,ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN&
  boundingBox=20,72,6,86&  # north,west,south,east (lat,lon)
  start=20000101&end=20241231&
  format=CSV&units=metric
```

3) Monthly and climatology summaries
```
# Monthly summaries by grid cell
https://power.larc.nasa.gov/api/temporal/monthly/region?community=ag&parameters=T2M,PRECTOTCORR&boundingBox=20,72,6,86&start=200001&end=202412&format=CSV&units=metric

# Long-term monthly normals
https://power.larc.nasa.gov/api/temporal/climatology/region?community=ag&parameters=T2M,PRECTOTCORR&boundingBox=20,72,6,86&format=CSV&units=metric
```

Implementation tips
- Use pagination/chunking by year or multi-year spans to respect limits.
- Add retries with exponential backoff and `-L` for redirects (if using curl).
- Prefer CSV for bulk and JSON for quick spot-checks.

## Processing Plan (cron_job.py)
1) Acquire
- Loop over parameters and time windows, calling region endpoints.
- Save raw CSVs with consistent paths and names.

2) Aggregate
- Convert daily series to monthly means (temps, humidity, wind, irradiance) and monthly totals (precipitation).
- Compute event probabilities, e.g., rainy-day fraction with threshold ≥1 mm/day.

3) Derive
- Cloud fraction = `1 - (ALLSKY / CLRSKY)` (bounded 0–1) if direct cloud amount unavailable.
- Comfort bands and "mild" scores from `T2M`/`T2M_MIN`/`T2M_MAX`.
- Agriculture advisor: Growing Degree Days (GDD), frost-day counts (`T2M_MIN <= 0°C`).

4) Store (GeoTIFF cache)
- One GeoTIFF per parameter×month (and derived layers) for the target region.
- Suggested naming: `<param>__<agg>__m<MM>.tif` (e.g., `T2M__mean__m01.tif`, `PRECTOTCORR__sum__m07.tif`).
- Embed metadata: source (POWER), period (years aggregated), units, and generation date.

5) Serve
- Backend reads GeoTIFFs to compute vibe scores for heatmaps ("Where") and monthly calendars ("When").

## Validation & Quality
- Sanity-check a few grid cells against point queries.
- Verify units and date alignment; ensure leap-year handling.
- Keep a manifest (JSON) listing files, stats, and date ranges for reproducibility.

## Next Steps
- Finalize bounding boxes (AOIs) and the baseline aggregation period (e.g., 2000–2020).
- Lock parameter list per vibe and advisor; confirm any thresholds (e.g., rainy day ≥1 mm, mild = 18–25°C).
- Implement `cron_job.py` with retries, chunking, and a small test suite.

