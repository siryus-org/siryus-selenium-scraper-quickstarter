import logging
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils.config import STAGE, has_display, url, download_dir, page_max_timeout
import psutil


def get_driver():
    route = ChromeDriverManager().install()
    options = Options()

    if STAGE == "production" or not has_display():
        options.add_argument("--headless")

    # Variables to not be detected as a bot
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extension")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--password-store=basic")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-translate")

    exp_opt = [
        # Disable possible errors
        "enable_automation",
        "ignore-certificate-errors",
        "enable-logging"
    ]
    options.add_experimental_option("excludeSwitches", exp_opt)

    pref_opt = {
        # Disable all type of popups
        "profile.default_content_setting_values.notifications": 2,
        "profile.password_manager_enabled": False,
        "intl.accept_languages": ["es-Es", "es"],
        "credentials_enable_service": False,

        # Automatic downloads
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        # Optional: Open PDFs in a separate viewer
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", pref_opt)

    # Init driver
    service = Service(route)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_page():
    # Return driver
    logging.info('Starting driver')
    driver = get_driver()
    logging.info('Getting URL')
    driver.get(url)
    return driver


def get_wait(driver):
    # Return wait function
    return WebDriverWait(driver, page_max_timeout)


def close_driver(driver):
    if driver:
        driver.quit()


# This function, kill all chrome process
def kill_driver_process():
    for proc in psutil.process_iter():
        try:
            if proc.name() == "chrome" or proc.name() == "chromedriver" or proc.name() == "chrome.exe":
                proc.kill()
        except psutil.NoSuchProcess:
            pass
