import os
import platform
from dotenv import load_dotenv

# Carga el .env desde la ruta absoluta
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def _env_bool(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# Global variables
STAGE = (os.getenv("STAGE") or 'staging').lower()
VALID_TOKEN = os.getenv("VALID_TOKEN") or ("sample" if STAGE != "production" else None)
AUTO_DELETE_LOGS = _env_bool("AUTO_DELETE_LOGS", True)
HEADLESS_MODE = os.getenv("HEADLESS_MODE") or 'auto'
BROWSER_LANGUAGE = os.getenv("BROWSER_LANGUAGE") or 'en'
DOWNLOAD_DIR = os.path.abspath(os.getenv("DOWNLOAD_DIR", "temp_downloads"))
PORT = int(os.getenv("PORT", 3000))
METRICS_PORT = int(os.getenv("METRICS_PORT", 9090))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
MAX_DOWNLOAD_BYTES = int(os.getenv("MAX_DOWNLOAD_BYTES", 20 * 1024 * 1024))
PAGE_MAX_TIMEOUT = int(os.getenv("PAGE_MAX_TIMEOUT", 7))
DOWNLOAD_MAX_TIMEOUT = int(os.getenv("DOWNLOAD_MAX_TIMEOUT", 4))
BASE_URL = os.getenv("BASE_URL", 'https://www.google.com/')
LOG_FILE_DELETION_DAYS = int(os.getenv("LOG_FILE_DELETION_DAYS", 30))


def validate_runtime_configuration():
    if STAGE == "production" and (not VALID_TOKEN or VALID_TOKEN == "sample"):
        raise RuntimeError(
            "VALID_TOKEN must be set to a non-default value in production"
        )

def has_display():
    if HEADLESS_MODE == 'True' or os.getenv("DOCKERIZED"):
        return False

    # ⬇️ Automatic mode
    system = platform.system()
    if system == "Windows":
        try:
            from screeninfo import get_monitors
            monitors = get_monitors()
            return len(monitors) > 0
        except ImportError:
            return False
    elif system == "Linux" or system == "Darwin":
        display_env = os.environ.get("DISPLAY")
        return display_env is not None
    else:
        # Other operating systems, we assume that there is no screen available
        return False
