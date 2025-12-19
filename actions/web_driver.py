import logging
import os
import inspect
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils.config import PAGE_MAX_TIMEOUT, BASE_URL, DOWNLOAD_DIR, STAGE, BROWSER_LANGUAGE, has_display
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import psutil


def get_driver_chrome():
    options = Options()
    options = add_generic_arguments(options)
    options = add_chrome_arguments(options)

    # Set the Chrome binary location (required when Chrome is not in default location)
    # In Alpine Linux, chromium is installed instead of google-chrome
    is_dockerized = os.environ.get(
        'DOCKERIZED', '').lower() in ('true', '1', 'yes')
    
    if is_dockerized or os.path.exists('/usr/bin/chromium'):
        options.binary_location = '/usr/bin/chromium'
    elif os.path.exists('/usr/bin/google-chrome'):
        options.binary_location = '/usr/bin/google-chrome'
    elif os.path.exists('/usr/bin/chromium-browser'):
        options.binary_location = '/usr/bin/chromium-browser'
    # else: let Selenium find it automatically

    # Check if running in Docker/production environment
    has_system_chromedriver = os.path.exists('/usr/bin/chromedriver')
    is_production = STAGE == 'production'

    # In Docker/Alpine environment, use the system chromium and chromedriver
    if is_dockerized or has_system_chromedriver or is_production:
        logging.debug("Using Docker/production chromedriver path")
        service = Service('/usr/bin/chromedriver')
    else:
        # Use webdriver-manager to download and manage chromedriver automatically
        logging.debug("Using webdriver-manager to download chromedriver")
        try:
            chromedriver_path = ChromeDriverManager().install()
            logging.debug(f"Chromedriver installed at: {chromedriver_path}")
            service = Service(chromedriver_path)
        except Exception as e:
            logging.warning(f"Failed to use webdriver-manager: {e}")
            # Fallback: Let Selenium find the browser automatically
            logging.debug("Using Selenium auto-discovery for chromedriver")
            service = None

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_driver_firefox():
    options = webdriver.FirefoxOptions()
    options = add_generic_arguments(options)
    driver = webdriver.Firefox(options=options)
    return driver


def get_page(browser='chrome', url=BASE_URL):
    # Return driver
    logging.info('Starting driver')
    if browser == 'firefox':
        driver = get_driver_firefox()
    else:
        driver = get_driver_chrome()
    logging.info('Getting URL')
    driver.get(url)
    return driver


def get_wait(driver):
    # Return wait function
    return WebDriverWait(driver, PAGE_MAX_TIMEOUT)


def close_driver(driver):
    """
    Cierra el driver de Selenium de forma segura.
    Maneja alertas abiertas, limpia eventos de JavaScript y proporciona logging detallado.

    Args:
        driver: Instancia del driver de Selenium

    Raises:
        Exception: Si ocurre un error al cerrar el driver
    """
    try:
        if driver:
            logging.info("Cerrando el driver...")

            # Limpiar eventos de beforeunload para evitar diálogos
            try:
                logging.info("Deshabilitando eventos beforeunload...")
                driver.execute_script("window.onbeforeunload = null;")
                logging.debug(
                    "Eventos beforeunload deshabilitados exitosamente")
            except Exception as js_error:
                logging.debug(
                    f"No se pudo deshabilitar beforeunload: {js_error}")

            # Limpiar unload handlers
            try:
                logging.debug("Deshabilitando eventos unload...")
                driver.execute_script("window.onunload = null;")
            except Exception as js_error:
                logging.debug(f"No se pudo deshabilitar unload: {js_error}")

            # Intentar cerrar cualquier alerta abierta antes de cerrar el driver
            try:
                alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
                logging.info("Alerta detectada, aceptando...")
                alert.accept()
            except Exception as alert_error:
                # No hay alerta presente, continuar con el cierre
                logging.debug(f"No hay alerta abierta: {alert_error}")

            # Cerrar todas las ventanas
            logging.info("Cerrando todas las ventanas del driver...")
            driver.quit()
            logging.info("Driver cerrado exitosamente")
        else:
            logging.warning("El driver es None, no se puede cerrar")
    except Exception as e:
        logging.error(
            f"Error {inspect.currentframe().f_code.co_name}: {e}", exc_info=True)


# This function, kill all chrome process
def kill_driver_process():
    for proc in psutil.process_iter():
        try:
            if proc.name() == "chrome" or proc.name() == "chromedriver" or proc.name() == "chrome.exe":
                proc.kill()
        except psutil.NoSuchProcess:
            pass


def add_generic_arguments(options):
    # Force headless mode - X11 in dev container doesn't work reliably with Chrome
    if not has_display():
        logging.info("Running in headless mode")
        options.add_argument("--headless")
    else:
        logging.info("Running in GUI mode")

    # Set language based on BROWSER_LANGUAGE configuration
    if BROWSER_LANGUAGE.lower() == 'es':
        language_arg = "--lang=es-ES"
    else:
        language_arg = "--lang=en-US"
    options.add_argument(language_arg)
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extension")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--password-store=basic")
    options.add_argument("--no-sandbox")
    # Prevenir cierre en contenedores
    options.add_argument("--disable-setuid-sandbox")
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
    
    # Evitar detección
    options.add_argument("--disable-blink-features=AutomationControlled")
    return options


def add_chrome_arguments(options):
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

    # Set language based on BROWSER_LANGUAGE configuration
    if BROWSER_LANGUAGE.lower() == 'es':
        language_list = ["es-ES", "es"]
    else:
        language_list = ["en-US", "en"]

    pref_opt = {
        # Disable all type of popups
        "profile.default_content_setting_values.notifications": 2,
        "profile.password_manager_enabled": False,
        "intl.accept_languages": language_list,
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
