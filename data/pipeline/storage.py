"""Utilities to persist raw downloads and metadata."""
from __future__ import annotations

import datetime as dt
import logging
from pathlib import Path
from typing import Optional

LOGGER = logging.getLogger(__name__)


class RawDataWriter:
    """Writes raw API responses to structured directories."""

    def __init__(self, base_dir: Path, create_dirs: bool = True) -> None:
        self.base_dir = base_dir
        if create_dirs:
            self.raw_dir.mkdir(parents=True, exist_ok=True)
            self.meta_dir.mkdir(parents=True, exist_ok=True)

    @property
    def raw_dir(self) -> Path:
        return self.base_dir / "raw"

    @property
    def meta_dir(self) -> Path:
        return self.base_dir / "manifests"

    def write(self, *, area: str, years: str, suffix: str, content: bytes) -> Path:
        timestamp = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = f"{area}__{years}__{timestamp}.{suffix}"
        target = self.raw_dir / filename
        LOGGER.info("Writing %s", target)
        target.write_bytes(content)
        return target

    def write_manifest(self, name: str, content: str) -> Path:
        target = self.meta_dir / name
        target.write_text(content, encoding="utf-8")
        return target
