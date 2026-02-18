import inspect
import logging
import time
from utils.config import PAGE_MAX_TIMEOUT
from utils.error import messageError
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def reload_driver(driver):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:
        logging.info("Recargando la página...")

        # Primero, deshabilitar cualquier evento beforeunload que dispara el diálogo
        logging.info("Deshabilitando eventos beforeunload...")
        driver.execute_script("window.onbeforeunload = null;")
        time.sleep(0.2)

        # Manejar cualquier alerta ya abierta
        try:
            alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
            logging.info("Alert detected, accepting it...")
            alert.accept()
            time.sleep(0.5)
        except Exception:
            # No hay alerta nativa, continuar
            pass

        # Usar JavaScript para recargar la página
        logging.info("Ejecutando recarga vía JavaScript...")
        driver.execute_script("window.location.reload();")

        # Esperar a que la página esté completamente cargada
        wait = WebDriverWait(driver, PAGE_MAX_TIMEOUT)
        wait.until(lambda d: d.execute_script(
            'return document.readyState') == 'complete')

        # Pequeño delay adicional para Docker/headless mode
        time.sleep(0.5)

        logging.info("Página recargada exitosamente")
    
        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
