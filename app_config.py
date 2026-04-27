import json
from pathlib import Path


APP_CONFIG_FILE = "app_config.json"


def get_app_config_path() -> Path:
    return Path(__file__).resolve().parent / APP_CONFIG_FILE


def load_app_config() -> dict:
    path = get_app_config_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_app_config(config: dict):
    path = get_app_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False, sort_keys=True)


def get_configured_username(default: str = "") -> str:
    config = load_app_config()
    username = str(config.get("username", "")).strip()
    return username or default


def set_configured_username(username: str):
    config = load_app_config()
    config["username"] = username.strip()
    save_app_config(config)
