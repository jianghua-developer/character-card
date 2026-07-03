import yaml
import sys
from pathlib import Path
from typing import Any, Dict
from util.resource_path import get_resource_path

_config_cache: Dict[str, Any] | None = None


def _get_config_path() -> Path:

    exe_dir = (
        Path(sys.executable).parent
        if getattr(sys, "frozen", False)
        else Path(__file__).parent.parent
    )
    external_config = exe_dir / "config.yml"
    if external_config.exists():
        return external_config
    return get_resource_path("config.yml")


def _load_config() -> Dict[str, Any]:
    global _config_cache

    if _config_cache is not None:
        return _config_cache

    config_path = _get_config_path()

    if not config_path.exists():
        _config_cache = {}
        return _config_cache

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            _config_cache = yaml.safe_load(f) or {}
    except Exception:
        _config_cache = {}

    return _config_cache


def get_config_value(config_name: str, default: Any) -> Any:
    config = _load_config()
    return config.get(config_name, default)
