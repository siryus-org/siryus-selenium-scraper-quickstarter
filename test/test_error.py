"""
Pruebas para el archivo error.py
"""
from utils.error import messageError
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def test_message_error_creation():
    """Verifica que se puede crear una excepción messageError"""
    error_msg = "Test error message"
    error = messageError(error_msg)
    assert str(error) == error_msg


def test_message_error_is_exception():
    """Verifica que messageError es una Exception"""
    error = messageError("Test")
    assert isinstance(error, Exception)


def test_message_error_can_be_raised():
    """Verifica que messageError puede ser lanzada como excepción"""
    with pytest.raises(messageError) as exc_info:
        raise messageError("Custom error message")
    assert "Custom error message" in str(exc_info.value)


def test_message_error_can_be_caught():
    """Verifica que messageError puede ser capturada"""
    try:
        raise messageError("Error to catch")
    except messageError as e:
        assert "Error to catch" in str(e)
    except Exception:
        pytest.fail("messageError should be caught as messageError")


def test_message_error_with_empty_message():
    """Verifica que messageError funciona con mensaje vacío"""
    error = messageError("")
    assert str(error) == ""


def test_message_error_with_special_characters():
    """Verifica que messageError maneja caracteres especiales"""
    special_msg = "Error: Field 'username' is required! @#$%"
    error = messageError(special_msg)
    assert str(error) == special_msg


def test_message_error_with_multiline():
    """Verifica que messageError maneja mensajes multilínea"""
    multiline_msg = "Error en línea 1\nError en línea 2\nError en línea 3"
    error = messageError(multiline_msg)
    assert str(error) == multiline_msg


def test_message_error_inheritance():
    """Verifica que messageError hereda de Exception"""
    assert issubclass(messageError, Exception)
