import os
import platform
from dotenv import load_dotenv
load_dotenv()
# Global variables
STAGE = os.getenv("STAGE") or 'staging'
VALID_TOKEN = os.getenv("VALID_TOKEN") or 'sample'
URL = "https://www.google.com/"  # Change this to target url
DOWNLOAD_DIR_NAME = 'temp_downloads'
from utils.file_manager import create_download_directory
DOWNLOAD_DIR = create_download_directory(DOWNLOAD_DIR_NAME)



PAGE_MAX_TIMEOUT = 7
DOWNLOAD_MAX_TIMEOUT = 4


def has_display():
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
