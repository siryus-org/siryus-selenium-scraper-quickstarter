"""Start a browser for interactive work in a Python terminal."""

import atexit

from dotenv import load_dotenv
from selenium_scraper_runtime.browser import close_driver, get_page, get_wait


load_dotenv()
driver = get_page()
atexit.register(close_driver, driver)
wait = get_wait(driver)
