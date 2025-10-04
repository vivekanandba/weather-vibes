# Offline Data Pack

This note captures everything bundled for offline analysis of NASA POWER data.

## Coverage
- 12 point locations tuned to Weather Vibes personas (Bangalore, Ooty, Coorg, Goa, Bandipur, Munnar, Mysore, Hampi, Pondicherry, Kodaikanal, Chikmagalur, Wayanad).
- Daily history: 2000-01-01 through 2024-12-31.
- Parameters: `T2M`, `T2M_MIN`, `T2M_MAX`, `RH2M`, `PRECTOTCORR`, `WS2M`, `ALLSKY_SFC_SW_DWN`, `CLRSKY_SFC_SW_DWN`, `T2MDEW` (see `data/config/power_parameters.yml`).

## Directory Layout
```
data/
  outputs/
    <area_key>/
      raw/                     # NASA POWER JSON chunks (3-year slices)
      monthly/
        csv/                   # Monthly metric tables per chunk
        <area_key>__monthly_summary.csv
    manifests/
      offline_manifest.json    # Coverage + size metadata
  weather_vibes_power_points.tar.gz  # Archive of the entire outputs/ tree
```

Key references:
- Area definitions: `data/config/areas_of_interest.yml`
- Offline manifest: `data/outputs/manifests/offline_manifest.json`
- Packed archive: `data/weather_vibes_power_points.tar.gz`

## Derived Metrics
Monthly tables add:
- `CLOUD_FRACTION` (1 − `ALLSKY`/`CLRSKY`, clamped 0–1)
- `RAINY_DAY_COUNT` and `RAINY_DAY_FRACTION` (threshold ≥ 1 mm)
- `MILD_SCORE` (100 inside 18–25 °C band, tapering outward)
- `STARGAZING_SCORE` (low cloud fraction × low humidity)

## Regeneration Workflow
1. Download daily chunks (JSON) per area:
   ```bash
   .venv/bin/python data/cron_job.py 2000 2024 \
     --area <area_key> --output-format JSON --output-dir data/outputs/<area_key>
   ```
2. Aggregate to monthly CSVs + manifest updates:
   ```bash
   .venv/bin/python data/aggregate_points.py --log-level INFO
   .venv/bin/python - <<'PY'
   from pathlib import Path
   from data.pipeline.config import load_pipeline_config
   import json, datetime as dt

   base = Path('data')
   config = load_pipeline_config(base)
   manifest = {
       'generated_at': dt.datetime.now(dt.UTC).isoformat(),
       'parameters': [p.id for p in config.parameters],
       'areas': {}
   }
   for key, area in config.areas.items():
       entry = {'name': area.name, 'type': 'region' if area.bounding_box else 'point'}
       out_dir = base / 'outputs' / key
       raw_dir = out_dir / 'raw'
       if raw_dir.exists():
           files = sorted(raw_dir.glob('*.json'))
           entry['raw_files'] = len(files)
           entry['raw_total_bytes'] = sum(f.stat().st_size for f in files)
           if files:
               entry['first_range'] = files[0].name.split('__')[1]
               entry['last_range'] = files[-1].name.split('__')[1]
       monthly_csv = out_dir / 'monthly' / f'{key}__monthly_summary.csv'
       if monthly_csv.exists():
           entry['monthly_summary_csv'] = str(monthly_csv.relative_to(base))
       manifest['areas'][key] = entry
   manifest_path = base / 'outputs' / 'manifests' / 'offline_manifest.json'
   manifest_path.parent.mkdir(parents=True, exist_ok=True)
   manifest_path.write_text(json.dumps(manifest, indent=2))
   PY
   ```
3. Package for travel:
   ```bash
   tar -czf data/weather_vibes_power_points.tar.gz -C data outputs
   ```

Parquet exports are skipped unless `pyarrow` or `fastparquet` is installed. Install with `.venv/bin/pip install pyarrow` before re-running the aggregator if parquet is required.

## Usage Tips
- Inspect a monthly summary quickly: `head data/outputs/bandipur_point/monthly/bandipur_point__monthly_summary.csv`
- Decompress the archive offline: `tar -xzf weather_vibes_power_points.tar.gz` (run inside the `data/` directory).
- When the POWER region endpoint is accessible again, extend this pipeline to produce gridded GeoTIFF layers for the "Where" feature.
