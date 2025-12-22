#!/usr/bin/env python
"""
Script de prueba visual - Abre Chrome/Firefox realmente y navega en headless
"""

from utils.file_manager import take_screenshot
from actions.web_driver import get_page, close_driver
import sys
import os
import time
import logging

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO)


def test_visual_navigation():
    """Prueba visual simple: abre Chrome en headless y navega"""

    print("\n" + "="*80)
    print("🎬 PRUEBA VISUAL - NAVEGACIÓN EN HEADLESS")
    print("="*80)

    # Forzar headless para WSL
    os.environ['HEADLESS_MODE'] = 'True'

    print("\n✨ Abriendo Chrome en modo headless...")

    driver = None
    try:
        # Abrir Chrome
        driver = get_page(browser='chrome', url='https://www.google.com')
        print("✅ Chrome abierto exitosamente!")
        print(f"   Título actual: {driver.title}")
        print(f"   URL: {driver.current_url}")

        # Esperar un poco para ver la página
        print("\n⏳ Esperando 3 segundos...")
        time.sleep(3)

        # Tomar screenshot de Google
        print("\n📸 Tomando screenshot de Google...")
        screenshot1 = take_screenshot(driver, "logs")
        print(f"   ✅ Guardado: {screenshot1}")

        # Navegar a GitHub
        print("\n🌐 Navegando a GitHub...")
        driver.get('https://www.github.com')
        time.sleep(3)
        print(f"   Título: {driver.title}")
        print(f"   URL: {driver.current_url}")

        # Tomar screenshot de GitHub
        print("\n📸 Tomando screenshot de GitHub...")
        screenshot2 = take_screenshot(driver, "logs")
        print(f"   ✅ Guardado: {screenshot2}")

        # Navegar de vuelta a Google
        print("\n🌐 Navegando de vuelta a Google...")
        driver.get('https://www.google.com')
        time.sleep(3)

        # Tomar screenshot final
        print("\n📸 Tomando screenshot final...")
        screenshot3 = take_screenshot(driver, "logs")
        print(f"   ✅ Guardado: {screenshot3}")

        print("\n" + "="*80)
        print("✅ PRUEBA VISUAL COMPLETADA EXITOSAMENTE")
        print("="*80)
        print("\n📸 Screenshots generados:")
        print(f"   1. {screenshot1}")
        print(f"   2. {screenshot2}")
        print(f"   3. {screenshot3}")
        print("\n" + "="*80 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if driver:
            print("\n🔄 Cerrando Chrome...")
            close_driver(driver)
            print("✅ Chrome cerrado")


if __name__ == '__main__':
    success = test_visual_navigation()
    sys.exit(0 if success else 1)
