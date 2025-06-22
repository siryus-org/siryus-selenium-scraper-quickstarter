"""
Pruebas para el archivo main.py usando pytest y Flask.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import app

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

def test_sample_endpoint(client):
    """Prueba el endpoint /sample con autenticación Bearer 'sample' y datos mínimos"""
    headers = {"Authorization": "Bearer sample"}
    # Se envía un body JSON con los campos requeridos por controller_sample
    data = {"username": "test", "password": "test"}
    response = client.get('/sample', headers=headers, json=data)
    assert response.status_code == 200
    # Se puede ajustar el contenido esperado según la lógica de controller_sample
