import inspect
import logging
from actions.web_driver import get_wait
from utils.error import messageError
from selenium.webdriver.support import expected_conditions

# This function searches for an element on the page, scrolls to it, and click to it.


def search_element(driver, locator, wait_to_be_clickable=True, raise_exception=True):
    # locator  example: By.CSS_SELECTOR, '[data-testid="login-submit-button"]'
    logging.info('- Access {}'.format(locator))
    wait = get_wait(driver)
    try:
        if wait_to_be_clickable:
            element = wait.until(expected_conditions.element_to_be_clickable((
                locator
            )))
        else:
            element = wait.until(expected_conditions.visibility_of_element_located((
                locator
            )))
        return element
    except Exception as e:
        if raise_exception:
            # Get information from the function that called Search_element
            caller = inspect.stack()[1]
            error_message = (
                f"Error in function '{caller.function}' at {caller.filename}:{caller.lineno} - "
                f"Failed to locate element {locator}: {str(e)}"
            )
            raise messageError(error_message)
        else:
            pass
