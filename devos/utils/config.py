import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".devos" / "config.json"

DEFAULT_CONFIG = {
    "watch_paths": [str(Path.home() / "Desktop")],
    "ignore_patterns": [".git", "__pycache__", ".venv", "node_modules"],
    "idle_timeout": 300,
    "theme": "dark"
}

def get_config():
    """Giving you the keys to the castle... :)"""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
        
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(config):
    """Locking the gates with your new settings"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def update_config(key, value):
    """Teaching the butler new tricks"""
    config = get_config()
    config[key] = value
    save_config(config)
