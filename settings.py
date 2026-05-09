"""Settings management using JSON in %APPDATA%."""

import json
import os
from pathlib import Path

DEFAULT_SETTINGS = {
    "save_mode": "suffix",
    "suffix": "-min",
    "custom_folder": "",
    "quality_min": 60,
    "quality_max": 80,
    "overwrite": False,
    "preserve_date": True,
    "open_folder_after": False,
}


def _get_settings_dir() -> Path:
    appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
    path = Path(appdata) / "PngTiny"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_settings_path() -> Path:
    return _get_settings_dir() / "settings.json"


def load_settings() -> dict:
    """Load settings, merging with defaults for missing keys."""
    settings = dict(DEFAULT_SETTINGS)
    path = _get_settings_path()

    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for key in DEFAULT_SETTINGS:
                if key in saved:
                    settings[key] = saved[key]
        except Exception:
            pass

    return settings


def save_settings(settings: dict) -> bool:
    """Persist settings to disk."""
    try:
        with open(_get_settings_path(), "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False
