"""
Pruebas para el archivo security.py
"""
from utils.security import authenticate_token
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


def test_authenticate_token_valid(client):
    """Verifica que un token válido es aceptado"""
    with app.test_request_context(headers={"Authorization": "Bearer sample"}):
        assert authenticate_token() == True


def test_authenticate_token_invalid(client):
    """Verifica que un token inválido es rechazado"""
    with app.test_request_context(headers={"Authorization": "Bearer invalid_token"}):
        assert authenticate_token() == False


def test_authenticate_token_missing(client):
    """Verifica que una petición sin token es rechazada"""
    with app.test_request_context():
        assert authenticate_token() == False


def test_authenticate_token_malformed(client):
    """Verifica que un token mal formado (sin 'Bearer ') es rechazado"""
    with app.test_request_context(headers={"Authorization": "sample"}):
        assert authenticate_token() == False


def test_authenticate_token_empty_bearer(client):
    """Verifica que un Bearer sin token es rechazado"""
    with app.test_request_context(headers={"Authorization": "Bearer "}):
        assert authenticate_token() == False


def test_authenticate_token_case_sensitive(client):
    """Verifica que el token es case-sensitive"""
    with app.test_request_context(headers={"Authorization": "Bearer SAMPLE"}):
        assert authenticate_token() == False


def test_authenticate_token_with_spaces(client):
    """Verifica que un token con espacios extra no funciona"""
    with app.test_request_context(headers={"Authorization": "Bearer  sample"}):
        assert authenticate_token() == False


def test_authenticate_token_lowercase_bearer(client):
    """Verifica que 'bearer' en minúsculas no funciona"""
    with app.test_request_context(headers={"Authorization": "bearer sample"}):
        assert authenticate_token() == False
