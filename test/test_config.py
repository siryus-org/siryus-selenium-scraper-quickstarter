"""
Pruebas para el archivo config.py
"""
from utils.config import LOG_FILE_DELETION_DAYS
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def test_log_file_deletion_days_exists():
    """Verifica que la variable LOG_FILE_DELETION_DAYS existe"""
    assert LOG_FILE_DELETION_DAYS is not None


def test_log_file_deletion_days_is_30():
    """Verifica que la variable LOG_FILE_DELETION_DAYS está configurada a 30 días"""
    assert LOG_FILE_DELETION_DAYS == 30


def test_log_file_deletion_days_is_integer():
    """Verifica que la variable LOG_FILE_DELETION_DAYS es un entero"""
    assert isinstance(LOG_FILE_DELETION_DAYS, int)


def test_log_file_deletion_days_is_positive():
    """Verifica que la variable LOG_FILE_DELETION_DAYS es un número positivo"""
    assert LOG_FILE_DELETION_DAYS > 0
