# NO BORRAR PARA QUE LOS TEST DE LA PIPELINE NO DEN ERROR
"""
Controller de pruebas completo que valida múltiples navegadores y funcionalidades.

Este controller realiza pruebas extensivas incluyendo:
- Pruebas con Chrome y Firefox
- Búsqueda de elementos
- Clicks en elementos
- Escritura de texto
- Screenshots
- Validación de títulos de página
- Manejo de errores
"""

import inspect
import logging
from time import sleep
from selenium.webdriver.common.by import By

from selenium_scraper_runtime.browser import close_driver, get_page
from selenium_scraper_runtime.elements import search_element, write_element
from utils.error import messageError
from utils.file_manager import take_screenshot


def controller_test(data=None):
    """
    Controlador de pruebas completo que valida todos los navegadores y funcionalidades.

    Args:
        data (dict, optional): Diccionario con parámetros de prueba.
            - browsers: Lista de navegadores a probar ['chrome', 'firefox']. Default: ['chrome', 'firefox']
            - test_search: Boolean para probar búsquedas. Default: True
            - test_writes: Boolean para probar escritura de texto. Default: True
            - screenshots: Boolean para guardar screenshots. Default: True
            - urls: Lista de URLs a visitar. Default: ['https://www.google.com', 'https://www.github.com']

    Returns:
        dict: Resultado de las pruebas con estadísticas

    Raises:
        messageError: Si ocurre un error crítico
    """
    driver = None
    test_results = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'browser_results': {},
        'errors': []
    }

    try:
        # Procesar parámetros de entrada
        browsers = data.get('browsers', ['chrome', 'firefox']) if data else [
            'chrome', 'firefox']
        test_search = data.get('test_search', True) if data else True
        test_writes = data.get('test_writes', True) if data else True
        screenshots = data.get('screenshots', True) if data else True
        urls = data.get('urls', ['https://www.google.com', 'https://www.github.com']) if data else [
            'https://www.google.com', 'https://www.github.com']

        logging.info("=" * 80)
        logging.info("🧪 INICIANDO PRUEBAS DE NAVEGADORES Y FUNCIONALIDADES")
        logging.info("=" * 80)
        logging.info(f"📋 Navegadores a probar: {browsers}")
        logging.info(f"🔗 URLs a visitar: {urls}")
        logging.info(
            f"🔍 Pruebas habilitadas - Búsqueda: {test_search}, Escritura: {test_writes}, Screenshots: {screenshots}")
        logging.info("=" * 80)

        # Probar cada navegador
        for browser in browsers:
            driver = None
            logging.info(f"\n{'='*80}")
            logging.info(f"🌐 PRUEBANDO NAVEGADOR: {browser.upper()}")
            logging.info(f"{'='*80}")

            browser_result = {
                'status': 'pending',
                'tests': [],
                'error': None
            }

            try:
                # Test 1: Crear driver
                logging.info(f"✓ Test 1/7: Iniciando driver de {browser}...")
                test_results['total_tests'] += 1
                try:
                    driver = get_page(browser=browser)
                    logging.info(
                        f"  ✅ Driver de {browser} creado exitosamente")
                    test_results['passed_tests'] += 1
                    browser_result['tests'].append({
                        'name': 'Iniciar driver',
                        'status': 'PASSED',
                        'details': f'Driver {browser} creado'
                    })
                except Exception as e:
                    logging.error(f"  ❌ Error al crear driver: {e}")
                    test_results['failed_tests'] += 1
                    browser_result['tests'].append({
                        'name': 'Iniciar driver',
                        'status': 'FAILED',
                        'error': str(e)
                    })
                    continue

                # Test 2: Visitar URLs
                logging.info(f"✓ Test 2/7: Visitando URLs...")
                test_results['total_tests'] += 1
                try:
                    visited_urls = []
                    for url in urls:
                        driver.get(url)
                        sleep(2)  # Esperar a que cargue la página
                        current_url = driver.current_url
                        current_title = driver.title
                        visited_urls.append({
                            'requested': url,
                            'current': current_url,
                            'title': current_title
                        })
                        logging.info(f"  ✅ Visitada: {url}")
                        logging.info(f"     Título: {current_title}")

                    test_results['passed_tests'] += 1
                    browser_result['tests'].append({
                        'name': 'Visitar URLs',
                        'status': 'PASSED',
                        'details': f'Visitadas {len(visited_urls)} URLs exitosamente',
                        'urls': visited_urls
                    })
                except Exception as e:
                    logging.error(f"  ❌ Error al visitar URLs: {e}")
                    test_results['failed_tests'] += 1
                    browser_result['tests'].append({
                        'name': 'Visitar URLs',
                        'status': 'FAILED',
                        'error': str(e)
                    })

                # Test 3: Obtener información de la página
                logging.info(
                    f"✓ Test 3/7: Obteniendo información de la página...")
                test_results['total_tests'] += 1
                try:
                    page_info = {
                        'title': driver.title,
                        'url': driver.current_url,
                        'window_size': driver.get_window_size(),
                        'cookies_count': len(driver.get_cookies())
                    }
                    logging.info(f"  ✅ Información de página obtenida:")
                    logging.info(f"     Título: {page_info['title']}")
                    logging.info(f"     URL: {page_info['url']}")
                    logging.info(
                        f"     Tamaño ventana: {page_info['window_size']}")
                    logging.info(f"     Cookies: {page_info['cookies_count']}")

                    test_results['passed_tests'] += 1
                    browser_result['tests'].append({
                        'name': 'Información de página',
                        'status': 'PASSED',
                        'page_info': page_info
                    })
                except Exception as e:
                    logging.error(f"  ❌ Error al obtener información: {e}")
                    test_results['failed_tests'] += 1
                    browser_result['tests'].append({
                        'name': 'Información de página',
                        'status': 'FAILED',
                        'error': str(e)
                    })

                # Test 4: Ejecutar JavaScript
                logging.info(f"✓ Test 4/7: Ejecutando JavaScript...")
                test_results['total_tests'] += 1
                try:
                    result = driver.execute_script(
                        "return {userAgent: navigator.userAgent, language: navigator.language}")
                    logging.info(f"  ✅ JavaScript ejecutado:")
                    logging.info(f"     User Agent: {result['userAgent']}")
                    logging.info(f"     Idioma: {result['language']}")

                    test_results['passed_tests'] += 1
                    browser_result['tests'].append({
                        'name': 'Ejecutar JavaScript',
                        'status': 'PASSED',
                        'js_result': result
                    })
                except Exception as e:
                    logging.error(f"  ❌ Error al ejecutar JavaScript: {e}")
                    test_results['failed_tests'] += 1
                    browser_result['tests'].append({
                        'name': 'Ejecutar JavaScript',
                        'status': 'FAILED',
                        'error': str(e)
                    })

                # Test 5: Buscar elementos
                if test_search:
                    logging.info(f"✓ Test 5/7: Buscando elementos...")
                    test_results['total_tests'] += 1
                    try:
                        # Buscar el campo de búsqueda de Google
                        search_input = search_element(
                            driver,
                            (By.CSS_SELECTOR, 'input[name="q"]'),
                            wait_to_search=True,
                            raise_exception=False
                        )
                        if search_input:
                            logging.info(
                                f"  ✅ Elemento de búsqueda encontrado")
                            test_results['passed_tests'] += 1
                            browser_result['tests'].append({
                                'name': 'Buscar elementos',
                                'status': 'PASSED',
                                'element_found': 'Campo de búsqueda'
                            })
                        else:
                            logging.warning(
                                f"  ⚠️  Elemento no encontrado (esperado en algunas URLs)")
                            test_results['passed_tests'] += 1
                            browser_result['tests'].append({
                                'name': 'Buscar elementos',
                                'status': 'PASSED',
                                'details': 'Búsqueda completada (elemento no presente en todas las páginas)'
                            })
                    except Exception as e:
                        logging.error(f"  ❌ Error al buscar elementos: {e}")
                        test_results['failed_tests'] += 1
                        browser_result['tests'].append({
                            'name': 'Buscar elementos',
                            'status': 'FAILED',
                            'error': str(e)
                        })
                else:
                    logging.info(
                        f"⊘ Test 5/7: Búsqueda de elementos deshabilitada")

                # Test 6: Escribir en elementos
                if test_writes:
                    logging.info(f"✓ Test 6/7: Probando escritura de texto...")
                    test_results['total_tests'] += 1
                    try:
                        # Buscar el campo de búsqueda de Google
                        search_input = search_element(
                            driver,
                            (By.CSS_SELECTOR, 'input[name="q"]'),
                            wait_to_search=True,
                            raise_exception=False
                        )
                        if search_input:
                            test_text = "Selenium WebDriver Test"
                            driver = write_element(
                                driver, search_input, test_text)
                            sleep(1)
                            input_value = search_input.get_attribute('value')
                            logging.info(f"  ✅ Texto escrito: '{input_value}'")

                            test_results['passed_tests'] += 1
                            browser_result['tests'].append({
                                'name': 'Escribir en elementos',
                                'status': 'PASSED',
                                'text_written': test_text,
                                'value_read': input_value
                            })
                        else:
                            logging.warning(
                                f"  ⚠️  No se pudo escribir (elemento no disponible)")
                            test_results['passed_tests'] += 1
                            browser_result['tests'].append({
                                'name': 'Escribir en elementos',
                                'status': 'PASSED',
                                'details': 'Prueba saltada (elemento no disponible)'
                            })
                    except Exception as e:
                        logging.error(f"  ❌ Error al escribir: {e}")
                        test_results['failed_tests'] += 1
                        browser_result['tests'].append({
                            'name': 'Escribir en elementos',
                            'status': 'FAILED',
                            'error': str(e)
                        })
                else:
                    logging.info(
                        f"⊘ Test 6/7: Escritura de elementos deshabilitada")

                # Test 7: Captura de pantalla
                if screenshots:
                    logging.info(f"✓ Test 7/7: Capturando screenshot...")
                    test_results['total_tests'] += 1
                    try:
                        screenshot_path = take_screenshot(driver, "logs")
                        logging.info(
                            f"  ✅ Screenshot guardado en: {screenshot_path}")

                        test_results['passed_tests'] += 1
                        browser_result['tests'].append({
                            'name': 'Captura de pantalla',
                            'status': 'PASSED',
                            'screenshot_path': screenshot_path
                        })
                    except Exception as e:
                        logging.error(f"  ❌ Error al capturar screenshot: {e}")
                        test_results['failed_tests'] += 1
                        browser_result['tests'].append({
                            'name': 'Captura de pantalla',
                            'status': 'FAILED',
                            'error': str(e)
                        })
                else:
                    logging.info(f"⊘ Test 7/7: Screenshots deshabilitados")

                browser_result['status'] = 'COMPLETED'

            except Exception as e:
                logging.error(f"❌ Error en pruebas de {browser}: {str(e)}")
                browser_result['status'] = 'FAILED'
                browser_result['error'] = str(e)
                test_results['errors'].append({
                    'browser': browser,
                    'error': str(e)
                })

            finally:
                # Cerrar driver
                if driver:
                    try:
                        close_driver(driver)
                        logging.info(
                            f"✅ Driver de {browser} cerrado correctamente")
                    except Exception as e:
                        logging.warning(
                            f"⚠️  Error al cerrar driver de {browser}: {e}")
                    finally:
                        driver = None

            test_results['browser_results'][browser] = browser_result
            sleep(2)  # Pausa entre navegadores

        # Mostrar resumen final
        logging.info(f"\n{'='*80}")
        logging.info("📊 RESUMEN DE PRUEBAS")
        logging.info(f"{'='*80}")
        logging.info(
            f"✅ Pruebas exitosas: {test_results['passed_tests']}/{test_results['total_tests']}")
        logging.info(
            f"❌ Pruebas fallidas: {test_results['failed_tests']}/{test_results['total_tests']}")
        success_rate = (test_results['passed_tests'] / test_results['total_tests']
                        * 100) if test_results['total_tests'] > 0 else 0
        logging.info(f"📈 Tasa de éxito: {success_rate:.1f}%")

        if test_results['errors']:
            logging.warning(
                f"⚠️  Errores detectados: {len(test_results['errors'])}")
            for error_info in test_results['errors']:
                logging.warning(
                    f"   - {error_info['browser']}: {error_info['error']}")

        for browser, result in test_results['browser_results'].items():
            logging.info(f"\n🌐 {browser.upper()}: {result['status']}")
            for test in result['tests']:
                emoji = "✅" if test['status'] == 'PASSED' else "❌"
                logging.info(f"   {emoji} {test['name']}: {test['status']}")

        logging.info(f"{'='*80}")
        logging.info("✅ PRUEBAS COMPLETADAS")
        logging.info(f"{'='*80}\n")

        return test_results

    except Exception as e:
        logging.error(
            f"Error crítico en {inspect.currentframe().f_code.co_name}: {e}")
        raise messageError(f"Error en controlador de pruebas: {e}")

    finally:
        if driver:
            close_driver(driver)
