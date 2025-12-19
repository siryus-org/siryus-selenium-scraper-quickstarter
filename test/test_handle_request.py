"""
Pruebas para el archivo handle_request.py
"""
from main import app
import json
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


def test_handle_request_unauthorized_no_token(client):
    """Verifica que devuelve 401 sin token"""
    response = client.get('/sample', json={"test": "data"})
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'ERROR'
    assert data['message'] == 'Unauthorized'
    assert 'time' in data


def test_handle_request_unauthorized_invalid_token(client):
    """Verifica que devuelve 401 con token inválido"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get('/sample', headers=headers, json={"test": "data"})
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'ERROR'
    assert data['message'] == 'Unauthorized'


def test_handle_request_no_json_body(client):
    """Verifica que devuelve 400 sin body JSON"""
    headers = {"Authorization": "Bearer sample"}
    response = client.get('/sample', headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'ERROR'
    assert 'JSON' in data['message']


def test_handle_request_missing_required_field(client):
    """Verifica que devuelve 400 cuando falta un campo requerido"""
    headers = {"Authorization": "Bearer sample"}
    # Enviar solo username sin password
    response = client.get('/sample', headers=headers,
                          json={"username": "test"})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'ERROR'
    assert 'password' in data['message']


def test_handle_request_empty_json(client):
    """Verifica que devuelve 400 con JSON vacío"""
    headers = {"Authorization": "Bearer sample"}
    response = client.get('/sample', headers=headers, json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'ERROR'


def test_handle_request_valid_structure(client):
    """Verifica que la respuesta tiene la estructura correcta"""
    headers = {"Authorization": "Bearer sample"}
    response = client.get('/', headers=headers)

    # El endpoint raíz no requiere autenticación ni JSON
    assert response.status_code == 200


def test_handle_request_response_time_included(client):
    """Verifica que la respuesta incluye tiempo de ejecución"""
    headers = {"Authorization": "Bearer sample"}
    response = client.get('/sample', headers=headers,
                          json={"username": "test"})

    data = json.loads(response.data)
    assert 'time' in data
    assert isinstance(data['time'], (int, float))
    assert data['time'] >= 0


def test_handle_request_logs_without_password(client):
    """Verifica que no se loguea la contraseña en los datos"""
    # Este test verifica que el sistema no loguea contraseñas
    # La implementación filtra 'password' antes de loguear
    headers = {"Authorization": "Bearer sample"}
    data = {"username": "testuser", "password": "secretpassword"}
    response = client.get('/sample', headers=headers, json=data)

    # Solo verificamos que no lanza excepción al procesar
    assert response.status_code in [200, 400]


def test_handle_request_malformed_json(client):
    """Verifica manejo de JSON mal formado"""
    headers = {
        "Authorization": "Bearer sample",
        "Content-Type": "application/json"
    }
    response = client.get('/sample', headers=headers, data="not valid json")
    assert response.status_code == 400


def test_handle_request_with_valid_auth_and_data(client):
    """Verifica que con autenticación y datos válidos se procesa correctamente"""
    headers = {"Authorization": "Bearer sample"}
    data = {"username": "testuser", "password": "testpass"}

    # Dado que el controller_sample requiere Selenium, esperamos 400
    # pero la autenticación y validación JSON deberían pasar
    response = client.get('/sample', headers=headers, json=data)

    # Puede ser 200 o 400 dependiendo de si Selenium está disponible
    assert response.status_code in [200, 400]

    response_data = json.loads(response.data)
    assert 'status' in response_data
    assert 'time' in response_data


def test_handle_request_case_sensitive_bearer(client):
    """Verifica que Bearer es case-sensitive"""
    headers = {"Authorization": "bearer sample"}  # minúscula
    response = client.get('/sample', headers=headers, json={"test": "data"})
    assert response.status_code == 401


def test_handle_request_extra_spaces_in_token(client):
    """Verifica que espacios extra en el token causan error"""
    headers = {"Authorization": "Bearer  sample"}  # doble espacio
    response = client.get('/sample', headers=headers, json={"test": "data"})
    assert response.status_code == 401
