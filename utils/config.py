from utils.file_manager import create_download_directory
import os
import platform

# Global variables
url = "https://www.google.com/" #Change this to target url

# If you need to 
download_dir_name = 'temp_downloads'

download_dir = create_download_directory(download_dir_name)

page_max_timeout = 7
download_max_timeout = 4


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
