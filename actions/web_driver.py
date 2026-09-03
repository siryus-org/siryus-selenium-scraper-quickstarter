import inspect
import logging
import os
import threading
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.config import PAGE_MAX_TIMEOUT, BASE_URL, DOWNLOAD_DIR, has_display
from selenium_stealth import stealth

import psutil


def get_driver_chrome():
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    options = Options()
    options = add_generic_arguments(options)
    options = add_chrome_arguments(options)

    # Set Chrome/Chromium binary location if found
    chrome_binary = get_chrome_binary()
    if chrome_binary:
        logging.info(f'Using Chrome binary: {chrome_binary}')
        options.binary_location = chrome_binary

    if (os.getenv("DOCKERIZED") == "true"):
        # When running with Docker Compose
        logging.info('Using local chromedriver')
        service = Service('/usr/bin/chromedriver')
    else:
        # For local development
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_driver_firefox():
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    options = FirefoxOptions()
    options = add_generic_arguments(options)
    options.accept_insecure_certs = True

    firefox_binary = get_firefox_binary()
    if firefox_binary:
        options.binary_location = firefox_binary

    service = None
    gecko_path = '/usr/bin/geckodriver'
    if os.environ.get('DOCKERIZED', False) or os.path.exists(gecko_path):
        # Prefer the packaged geckodriver inside containers to avoid Selenium Manager downloads
        if os.path.exists(gecko_path):
            service = FirefoxService(executable_path=gecko_path)

    if service:
        driver = webdriver.Firefox(service=service, options=options)
    else:
        driver = webdriver.Firefox(options=options)
    return driver


def get_page(browser='chrome', url=BASE_URL):
    logging.info(
        f"START || {inspect.currentframe().f_code.co_name} - Browser: {browser}, URL: {url}")

    driver = None
    try:
        if browser == 'firefox':
            driver = get_driver_firefox()
        else:
            driver = get_driver_chrome()
            stealth(
                driver,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
        logging.info('Getting URL')
        driver.get(url)
        return driver
    except Exception:
        # A browser can exist even when get_page() never returns it.
        close_driver(driver)
        raise


def get_wait(driver):
    # Return wait function
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    return WebDriverWait(driver, PAGE_MAX_TIMEOUT)


def _get_driver_processes(driver):
    """Return the service/browser process tree owned by this WebDriver."""
    try:
        service_process = driver.service.process
        if service_process is None:
            return []
        root_process = psutil.Process(service_process.pid)
        return root_process.children(recursive=True) + [root_process]
    except (AttributeError, psutil.Error):
        return []


def _terminate_processes(processes):
    processes = [process for process in processes if process.is_running()]
    for process in processes:
        try:
            process.terminate()
        except psutil.Error:
            pass

    _, alive = psutil.wait_procs(processes, timeout=2)
    for process in alive:
        try:
            process.kill()
        except psutil.Error:
            pass
    psutil.wait_procs(alive, timeout=2)


def close_driver(driver):
    """Close a driver without allowing hung browser processes to accumulate."""
    if driver is None:
        return

    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    processes = _get_driver_processes(driver)
    quit_errors = []

    def quit_driver():
        try:
            driver.quit()
        except Exception as error:
            quit_errors.append(error)

    quit_thread = threading.Thread(target=quit_driver, daemon=True)
    quit_thread.start()
    quit_thread.join(timeout=10)

    if quit_thread.is_alive():
        logging.warning('WebDriver quit timed out; terminating its process tree')
    elif quit_errors:
        logging.warning('WebDriver quit failed: %s', quit_errors[0])

    # quit() normally stops them. Only terminate processes belonging to this
    # driver when they survived the graceful close.
    _, alive = psutil.wait_procs(processes, timeout=2)
    if alive:
        _terminate_processes(alive)
    quit_thread.join(timeout=2)


# This function, kill all chrome process
def kill_driver_process():
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    for proc in psutil.process_iter():
        try:
            if proc.name() == "chrome" or proc.name() == "chromedriver" or proc.name() == "chrome.exe":
                proc.kill()
        except psutil.NoSuchProcess:
            pass


def add_generic_arguments(options):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    if not has_display():
        options.add_argument("--headless")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extension")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--password-store=basic")
    options.add_argument("--no-sandbox")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-translate")
    return options


def get_firefox_binary():
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    candidates = [
        os.environ.get("FIREFOX_BIN"),
        "/usr/bin/firefox",
        "/usr/bin/firefox-esr",
        "/usr/lib/firefox/firefox",
        "/usr/lib/firefox-esr/firefox-esr",
    ]
    return next((path for path in candidates if path and os.path.exists(path)), None)


def get_chrome_binary():
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    candidates = [
        os.environ.get("CHROME_BIN"),
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
    ]
    return next((path for path in candidates if path and os.path.exists(path)), None)


def add_chrome_arguments(options):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")
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
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        # Optional: Open PDFs in a separate viewer
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", pref_opt)

    return options
