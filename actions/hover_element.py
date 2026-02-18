import inspect
import logging
from time import sleep
from utils.error import messageError
from selenium.webdriver.common.action_chains import ActionChains


def hover_element(driver, element, pause_time=0.5):
    logging.info(f"START || {inspect.currentframe().f_code.co_name} - Element: {element}")
    """
    Realiza un hover (movimiento del mouse) sobre un elemento

    Args:
        driver: WebDriver de Selenium
        element: Elemento web sobre el que hacer hover
        pause_time: Tiempo de pausa después del hover (en segundos)

    Returns:
        driver: WebDriver de Selenium actualizado

    Raises:
        messageError: Si ocurre un error durante el hover
    """
    try:
        if element is None:
            raise ValueError("El elemento no puede ser None")

        # Scroll al elemento para asegurar que esté visible
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(0.3)

        # Crear las acciones de hover
        actions = ActionChains(driver)
        actions.move_to_element(element).pause(pause_time).perform()

        logging.info(f"Hover realizado exitosamente en el elemento")
        return driver

    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
