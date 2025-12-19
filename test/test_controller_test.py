"""
Pruebas para el controlador de pruebas (controller_test).

Tests para validar que el controller_test funciona correctamente con diferentes navegadores
y que ejecuta todas las funcionalidades esperadas.
"""

from controller.controller_test import controller_test
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session", autouse=True)
def cleanup_screenshots():
    """
    Limpia las capturas de pantalla después de ejecutar todos los tests.
    Se ejecuta automáticamente al final de la sesión de tests.
    """
    yield  # Ejecutar los tests primero

    # Limpiar después
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    if os.path.exists(logs_dir):
        try:
            # Eliminar solo archivos .png (screenshots)
            for filename in os.listdir(logs_dir):
                if filename.endswith('.png'):
                    filepath = os.path.join(logs_dir, filename)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                        print(f"✅ Limpiado: {filename}")
        except Exception as e:
            print(f"⚠️  Error al limpiar screenshots: {e}")


class TestControllerTest:
    """Suite de pruebas para controller_test"""

    def test_controller_test_returns_dict(self):
        """Test que verifica que el resultado es un diccionario válido"""
        test_data = {
            'browsers': ['chrome'],
            'test_search': False,
            'test_writes': False,
            'screenshots': False,
            'urls': ['https://www.google.com']
        }

        result = controller_test(test_data)

        # Validar estructura del resultado
        assert isinstance(result, dict)
        assert 'total_tests' in result
        assert 'passed_tests' in result
        assert 'failed_tests' in result
        assert 'browser_results' in result
        assert 'errors' in result

    def test_controller_test_browser_results_structure(self):
        """Test que valida la estructura de resultados por navegador"""
        test_data = {
            'browsers': ['chrome'],
            'test_search': False,
            'test_writes': False,
            'screenshots': False,
            'urls': ['https://www.google.com']
        }

        result = controller_test(test_data)

        # Validar estructura de resultados por navegador
        for browser, browser_result in result['browser_results'].items():
            assert isinstance(browser_result, dict)
            assert 'status' in browser_result
            assert 'tests' in browser_result
            assert isinstance(browser_result['tests'], list)

    def test_controller_test_multiple_urls(self):
        """Test que prueba múltiples URLs"""
        test_data = {
            'browsers': ['chrome'],
            'test_search': False,
            'test_writes': False,
            'screenshots': False,
            'urls': ['https://www.google.com', 'https://www.github.com']
        }

        result = controller_test(test_data)

        assert result is not None
        assert isinstance(result, dict)
        assert 'total_tests' in result

    def test_controller_test_with_firefox(self):
        """Test con Firefox en lugar de Chrome"""
        test_data = {
            'browsers': ['firefox'],
            'test_search': False,
            'test_writes': False,
            'screenshots': False,
            'urls': ['https://www.google.com']
        }

        result = controller_test(test_data)

        assert result is not None
        assert isinstance(result, dict)
        assert 'browser_results' in result

    def test_controller_test_visual_with_screenshots(self):
        """Test VISUAL - Abre navegador real, navega a URLs y toma screenshots

        ⚠️ Este test SÍ abre ventanas del navegador Chrome
        ⚠️ Verá navegación a Google y GitHub
        ⚠️ Se guardarán screenshots en logs/

        Requiere display disponible (DISPLAY=:0)
        """
        test_data = {
            'browsers': ['chrome'],
            'test_search': True,   # Buscar elementos en la página
            'test_writes': False,
            'screenshots': True,   # Tomar screenshots
            'urls': ['https://www.google.com', 'https://www.github.com']
        }

        print("\n" + "="*80)
        print("🎬 INICIANDO TEST VISUAL")
        print("   Se abrirá el navegador Chrome")
        print("   Se navegará a: Google y GitHub")
        print("   Se tomarán screenshots")
        print("="*80 + "\n")

        result = controller_test(test_data)

        # Validaciones
        assert result is not None
        assert isinstance(result, dict)
        assert 'total_tests' in result
        assert 'browser_results' in result

        print("\n" + "="*80)
        print("✅ TEST VISUAL COMPLETADO")
        print(f"   Total tests ejecutados: {result['total_tests']}")
        print(f"   Tests pasados: {result['passed_tests']}")
        print(f"   Tests fallidos: {result['failed_tests']}")
        print(f"   Screenshots guardados en: logs/")
        print("="*80 + "\n")


class TestControllerTestEndpoint:
    """Tests para el endpoint /test en Flask"""

    @pytest.fixture
    def client(self):
        from main import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_test_endpoint_exists(self, client):
        """Test que verifica que el endpoint /test existe"""
        headers = {"Authorization": "Bearer sample"}
        response = client.get('/test', headers=headers)

        # No debe ser 404
        assert response.status_code != 404

    def test_test_endpoint_without_auth(self, client):
        """Test que verifica que /test requiere autenticación"""
        response = client.get('/test')
        assert response.status_code == 401

    def test_test_endpoint_with_auth(self, client):
        """Test que verifica que /test funciona con autenticación"""
        headers = {"Authorization": "Bearer sample"}
        response = client.post('/test', headers=headers, json={})

        assert response.status_code != 401

    def test_test_endpoint_post_method(self, client):
        """Test que verifica que /test soporta POST"""
        headers = {"Authorization": "Bearer sample"}
        response = client.post('/test', headers=headers, json={})

        assert response.status_code in [200, 400, 500]


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
