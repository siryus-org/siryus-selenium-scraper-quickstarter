import inspect
import logging
from actions.click_element import click_element
from actions.web_driver import get_wait
from actions.write_element import write_element
from utils.error import messageError
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

# The driver must have accessed the target url
# TODO: Modify login for hacerlo coincide with the web site


def login(driver, username, password):
    try:
        wait = get_wait(driver)
        # THIS IS A SAMPLE!!

        logging.info('- Access the user field')
        try:
            user_input = wait.until(
                expected_conditions.visibility_of_element_located((
                    By.CSS_SELECTOR, 'input[placeholder="Escriba su correo electrónico"]'
                )))
            driver = write_element(driver, user_input, username)
        except Exception as e:
            raise messageError(
                "The user field in the login was not found: " + str(e))

        logging.info('- Access the password field')
        try:
            password_input = wait.until(expected_conditions.visibility_of_element_located((
                By.CSS_SELECTOR, 'input[type="password"][placeholder="Escriba su contraseña"]'
            )))
            driver = write_element(driver, password_input, password)
        except Exception as e:
            raise messageError(
                "The password field in the login was not found: " + str(e))

        logging.info('- Access the access button')
        try:
            button_input = wait.until(
                expected_conditions.visibility_of_element_located((
                    By.CSS_SELECTOR, '[data-testid="login-submit-button"]'
                )))
            driver = click_element(driver, button_input)
        except Exception as e:
            raise messageError(
                "The login button has not been found: " + str(e))

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
