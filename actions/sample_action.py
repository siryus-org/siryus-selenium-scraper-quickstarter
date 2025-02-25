import inspect
import logging
from actions.click_element import click_element
from actions.search_element import search_element
from utils.config import STAGE
from utils.error import messageError
from selenium.webdriver.common.by import By


def sample_action(driver):
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
                print("Skipping click")

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
