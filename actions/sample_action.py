import inspect
import logging
from actions.click_element import click_element
from actions.web_driver import get_wait
from utils.config import STAGE
from utils.error import messageError
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


def sample_action(driver):
    try:
        wait = get_wait(driver)
        logging.info('- Access add activity button')

        try:
            accept_button = wait.until(expected_conditions.element_to_be_clickable((
                By.XPATH, "//span[text()='Accept']"
            )))
            driver = click_element(driver, accept_button)
        except Exception as e:
            raise messageError(
                "The Accept button has not found: " + str(e))

        # Sample action of production action
        if STAGE == "production" or STAGE == "testing":
            logging.info(
                '- Access send button')
            try:
                # Wait for the table to be visible
                send_button = wait.until(expected_conditions.element_to_be_clickable((
                    By.XPATH, "//span[text()='Delete']"
                )))
                driver = click_element(driver, send_button)
            except Exception as e:
                raise messageError(
                    "The delete button has not found: " + str(e))
        else:
            logging.info(
                '- Skipping access send button')
            if STAGE != "production":
                print("Skipping click")

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
