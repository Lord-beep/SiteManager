from pathlib import Path
import sys


def get_app_directory() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


APP_DIR = get_app_directory()

DATA_DIR = APP_DIR / "data"
LOGS_DIR = APP_DIR / "logs"
CONFIG_DIR = APP_DIR / "config"

DATABASE_PATH = DATA_DIR / "sites.db"

MASTER_PASSWORD_PATH = CONFIG_DIR / "master_password.dat"
ENCRYPTION_KEY_PATH = CONFIG_DIR / "encryption.key"


def initialize_directories():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
