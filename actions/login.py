import inspect
from actions.click_element import click_element
from actions.search_element import search_element
from actions.write_element import write_element
from utils.error import messageError
from selenium.webdriver.common.by import By

# The driver must have accessed the target url
# TODO: Modify login for hacerlo coincide with the web site


def login(driver, username, password):
    try:
        # THIS IS A SAMPLE!!

        user_input = search_element(driver, (
            By.CSS_SELECTOR, 'input[placeholder="Escriba su correo electrónico"]'
        ))
        driver = write_element(driver, user_input, username)

        password_input = search_element(driver, (
            By.CSS_SELECTOR, 'input[type="password"][placeholder="Escriba su contraseña"]'
        ))
        driver = write_element(driver, password_input, password)

        button_input = search_element(driver, (
            By.CSS_SELECTOR, '[data-testid="login-submit-button"]'
        ))
        driver = click_element(driver, button_input)

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
