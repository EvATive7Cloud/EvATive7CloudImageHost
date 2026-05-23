from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

import yaml


DEFAULT_CONFIG = {
    "allowed_types": ["image/jpeg", "image/png", "image/webp"],
    "max_file_size": 5 * 1024 * 1024,
    "mount_path": "/imgs",
    "port": 8000,
}


@dataclass(slots=True, frozen=True)
class AppConfig:
    data_dir: Path
    image_dir: Path
    config_file: Path
    allowed_types: list[str]
    max_file_size: int
    mount_path: str
    port: int


def load_app_config(data_dir: str | Path | None = None) -> AppConfig:
    base_dir = Path(data_dir or os.environ.get("DATA_DIR") or "./data")
    base_dir.mkdir(parents=True, exist_ok=True)

    image_dir = base_dir / "imgs"
    image_dir.mkdir(parents=True, exist_ok=True)

    config_file = base_dir / "config.yml"
    if not config_file.exists():
        config_file.write_text(
            yaml.safe_dump(DEFAULT_CONFIG, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    try:
        config_data = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
    except Exception:
        config_data = {}

    merged = {**DEFAULT_CONFIG, **config_data}
    mount_path = str(merged["mount_path"]).strip() or DEFAULT_CONFIG["mount_path"]
    if not mount_path.startswith("/"):
        mount_path = f"/{mount_path}"

    return AppConfig(
        data_dir=base_dir,
        image_dir=image_dir,
        config_file=config_file,
        allowed_types=[str(item) for item in merged["allowed_types"]],
        max_file_size=int(merged["max_file_size"]),
        mount_path=mount_path,
        port=int(merged["port"]),
    )
