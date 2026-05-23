import json
import sys
from pathlib import Path


def get_version() -> str | None:
    """
    Get application version.

    Returns:
        Version string, or None if failed to read
    """
    metadata = get_metadata()
    return metadata.get("version") if metadata else None


def get_metadata() -> dict | None:
    """
    Read metadata.json file.

    Returns:
        Metadata dictionary, or None if failed to read
    """
    # Try multiple possible paths
    possible_paths = [
        # Packaged: relative to _MEIPASS (PyInstaller temp directory)
        Path(getattr(sys, "_MEIPASS", ".")) / "metadata.json",
    ]

    for path in possible_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                continue

    return None
