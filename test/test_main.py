"""
Pruebas para el archivo main.py usando pytest y Flask.
"""
from main import app
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Prueba el endpoint raíz /"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'selenium-scraper-quickstarter' in response.data


def test_sample_endpoint_without_auth(client):
    """Prueba el endpoint /sample sin autenticación (debe fallar)"""
    data = {"username": "test", "password": "test"}
    response = client.get('/sample', json=data)
    assert response.status_code == 401  # Unauthorized


def test_sample_endpoint_missing_data(client):
    """Prueba el endpoint /sample con autenticación pero sin datos requeridos"""
    headers = {"Authorization": "Bearer sample"}
    response = client.get('/sample', headers=headers, json={})
    assert response.status_code == 400  # Bad Request

# NOTA: El test del endpoint /sample con Selenium se omite en CI/CD porque
# requiere ChromeDriver y un navegador, lo cual no está disponible en el entorno de pruebas.
# Para tests de integración completos, se recomienda usar mocks o un entorno con Selenium instalado.
