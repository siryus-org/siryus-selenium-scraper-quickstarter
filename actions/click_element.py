from utils.error import messageError
from selenium.webdriver.common.action_chains import ActionChains


# This function searches for an element on the page, scrolls to it, and click to it.
def click_element(driver, element):
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element.click()
        return driver
    except Exception as e:
        raise messageError(f"Error click on {element.text}" + str(e))
