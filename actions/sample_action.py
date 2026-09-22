import inspect
import logging
from selenium_scraper_runtime.elements import click_element, search_element
from utils.config import STAGE
from utils.error import messageError
from selenium.webdriver.common.by import By


def sample_action(driver):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:
        accept_button = search_element(driver, (
            By.XPATH, "//span[text()='Accept']"
        ))
        driver = click_element(driver, accept_button)

        # Sample action of production action
        if STAGE == "production" or STAGE == "testing":
            send_button = search_element(driver, (
                By.XPATH, "//span[text()='Delete']"
            ))
            driver = click_element(driver, send_button)
        else:
            logging.info(
                '- Skipping access send button')
            if STAGE != "production":
                logging.info("Skipping click")

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
