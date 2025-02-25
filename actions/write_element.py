
import inspect
from time import sleep
from utils.error import messageError
from selenium.webdriver.common.action_chains import ActionChains


# This function searches for an element on the page, scrolls to it, and writes to it.
def write_element(driver, element, text, clear=True, slow=False):
    try:

        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        if clear:
            element.clear()
        if slow:
            for i in text:
                sleep(0.1)
                element.send_keys(i)
        else:
            element.send_keys(text)
        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
