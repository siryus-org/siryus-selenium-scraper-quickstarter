import inspect
import logging
from time import sleep
from utils.error import messageError
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)


# This function searches for an element on the page, scrolls to it, and click to it with multiple fallback strategies.
def click_element(driver, element, max_attempts=3):
    logging.info(f"START || {inspect.currentframe().f_code.co_name} - Element: {element}")
    """
    Realiza un click seguro en un elemento, intentando diferentes métodos con robustez mejorada

    Args:
        driver: WebDriver de Selenium
        element: Elemento a hacer click
        max_attempts: Número máximo de intentos (default: 3)

    Returns:
        driver: WebDriver actualizado

    Raises:
        messageError: Si todos los intentos de click fallan
    """
    try:

        # PASO 1: Intentar método básico primero (click simple)
        try:

            # Verificar que el elemento esté disponible
            element.is_displayed()

            # Scroll básico al elemento
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", element)

            # ActionChains básico con move_to_element (método original)
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            element.click()

            return driver

        except (ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            logging.debug(
                f"⚠️ Método básico falló: {e}, pasando a métodos avanzados")
        except Exception as e:
            logging.debug(
                f"⚠️ Error inesperado en método básico: {e}, pasando a métodos avanzados")

        for attempt in range(max_attempts):
            try:
                logging.info(
                    f"🔄 Intento avanzado {attempt + 1}/{max_attempts}")

                # Verificar que el elemento sigue siendo válido
                try:
                    element.is_displayed()
                except StaleElementReferenceException:
                    logging.warning(
                        "Elemento obsoleto detectado, saltando intento")
                    continue

                # Scroll al elemento con JavaScript más robusto
                try:
                    driver.execute_script("""
                        arguments[0].scrollIntoView({
                            behavior: 'smooth', 
                            block: 'center',
                            inline: 'center'
                        });
                    """, element)
                    sleep(0.5)
                except Exception as e:
                    logging.warning(f"Error en scroll avanzado: {e}")

                # Habilitar elemento usando make_element_interactable
                make_element_interactable(driver, element)
                sleep(0.2)

                # Método 1: Click con ActionChains mejorado
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                    return driver
                except (ElementNotInteractableException, ElementClickInterceptedException) as e:
                    logging.debug(f"ActionChains avanzado falló: {e}")

                # Método 2: Click directo
                try:
                    element.click()
                    return driver
                except (ElementNotInteractableException, ElementClickInterceptedException) as e:
                    logging.debug(f"Click directo avanzado falló: {e}")

                # Método 3: Click con JavaScript
                try:
                    driver.execute_script("arguments[0].click();", element)
                    return driver
                except Exception as e:
                    logging.debug(f"Click con JavaScript falló: {e}")

                # Método 4: Focus y Enter
                try:
                    driver.execute_script("arguments[0].focus();", element)
                    element.send_keys(Keys.ENTER)
                    return driver
                except Exception as e:
                    logging.debug(f"Focus y Enter falló: {e}")

                # Método 5: ActionChains avanzado con pausa
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(element).pause(
                        0.1).click().perform()
                    return driver
                except Exception as e:
                    logging.debug(f"ActionChains con pausa falló: {e}")

                # Si llegamos aquí, todos los métodos fallaron en este intento
                logging.warning(
                    f"⚠️ Todos los métodos avanzados fallaron en intento {attempt + 1}")

                if attempt < max_attempts - 1:  # Si no es el último intento
                    sleep(1)  # Esperar antes del siguiente intento

            except StaleElementReferenceException:
                logging.warning(
                    "Elemento obsoleto durante click avanzado, continuando...")
                continue
            except Exception as e:
                logging.warning(
                    f"Error inesperado en intento avanzado {attempt + 1}: {e}")
                if attempt < max_attempts - 1:
                    sleep(1)
                continue

        # Si llegamos aquí, todos los intentos fallaron
        logging.error("❌ Todos los intentos de click fallaron")
        raise messageError(
            "No se pudo hacer click en el elemento después de múltiples intentos")

    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")


def make_element_interactable(driver, element):
    """
    Intenta hacer un elemento interactuable removiendo restricciones comunes

    Args:
        driver: WebDriver de Selenium
        element: Elemento web a hacer interactuable

    Returns:
        bool: True si el elemento fue habilitado exitosamente
    """
    try:

        # Script para habilitar elemento
        result = driver.execute_script("""
            var element = arguments[0];
            
            try {
                // Quitar atributos restrictivos
                element.removeAttribute('disabled');
                element.removeAttribute('readonly');
                element.disabled = false;
                element.readOnly = false;
                
                // Quitar clases que pueden bloquear interacción
                var restrictiveClasses = [
                    'disabled', 'readonly', 'not-allowed', 'pointer-events-none',
                    'dp__input_readonly', 'dp__pointer', 'dp__disabled'
                ];
                
                restrictiveClasses.forEach(function(className) {
                    element.classList.remove(className);
                });
                
                // Habilitar estilos
                element.style.pointerEvents = 'auto';
                element.style.cursor = 'auto';
                element.style.opacity = '1';
                element.style.visibility = 'visible';
                element.style.display = 'block';
                
                // Si es un input, asegurar que sea de tipo text
                if (element.tagName.toLowerCase() === 'input') {
                    if (element.getAttribute('inputmode') === 'none') {
                        element.setAttribute('inputmode', 'text');
                    }
                    if (!element.type || element.type === 'hidden') {
                        element.setAttribute('type', 'text');
                    }
                }
                
                // Habilitar contenedores padre que puedan estar bloqueando
                var parent = element.parentElement;
                var levels = 0;
                while (parent && levels < 5) {
                    parent.removeAttribute('disabled');
                    parent.disabled = false;
                    parent.style.pointerEvents = 'auto';
                    
                    restrictiveClasses.forEach(function(className) {
                        parent.classList.remove(className);
                    });
                    
                    parent = parent.parentElement;
                    levels++;
                }
                
                return true;
                
            } catch (error) {
                console.error('Error habilitando elemento:', error);
                return false;
            }
        """, element)

        if result:
            return True
        else:
            logging.warning("No se pudo habilitar el elemento")
            return False

    except Exception as e:
        logging.error(f"Error en make_element_interactable: {e}")
        return False
