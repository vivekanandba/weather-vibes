# Data Pipeline Framework

This folder hosts the extraction and preprocessing framework for NASA POWER data used in Weather Vibes.

## Structure
- `config/`: YAML definitions for parameters, POWER options, and areas of interest.
- `pipeline/`: Importable Python modules (config loading, HTTP fetching, storage, aggregation).
- `cron_job.py`: Scriptable entry point for batch downloads (suitable for cron/Airflow).
- `outputs/`: Default destination for raw downloads (created on demand).

## Usage
```bash
cd data
python cron_job.py 2000 2020 --area south_india --dry-run
# For point extractions specify JSON format:
# python cron_job.py 2000 2024 --area bangalore_core_point --output-format JSON --output-dir outputs/bangalore
# After downloads, aggregate monthly summaries:
# python aggregate_points.py --log-level INFO
```

**Next steps**
- Implement authenticated retries/backoff in `pipeline.fetch.fetch_chunk`.
- Extend `pipeline.aggregation` with real scoring/GeoTIFF export logic.
- Integrate the outputs with the FastAPI backend caching layer.
