from utils.error import messageError
from selenium.webdriver.common.action_chains import ActionChains


# This function searches for an element on the page, scrolls to it, and writes to it.
def write_element(driver, element, text, clear=True):
    try:

        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        if clear:
            element.clear()
        element.send_keys(text)
        return driver
    except Exception as e:
        raise messageError(f"Error click on {element.text}" + str(e))
