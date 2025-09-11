"""
Pruebas para el archivo logging_config.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import tempfile
import shutil
from datetime import datetime, timedelta
from utils.logging_config import _clean_old_records_from_file
from utils.config import LOG_FILE_DELETION_DAYS


def test_log_file_deletion_days_import():
    """Verifica que LOG_FILE_DELETION_DAYS se importa correctamente en logging_config"""
    from utils.logging_config import LOG_FILE_DELETION_DAYS
    assert LOG_FILE_DELETION_DAYS == 30


def test_clean_old_records_from_file():
    """Prueba la función de limpieza de registros antiguos usando LOG_FILE_DELETION_DAYS"""
    # Crear un archivo temporal con logs de diferentes fechas
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_path = temp_file.name
        
        # Fecha actual
        current_date = datetime.now()
        # Fecha antigua (más de LOG_FILE_DELETION_DAYS días)
        old_date = current_date - timedelta(days=LOG_FILE_DELETION_DAYS + 5)
        # Fecha reciente (menos de LOG_FILE_DELETION_DAYS días)
        recent_date = current_date - timedelta(days=5)
        
        # Escribir logs con diferentes fechas
        temp_file.write(f"{old_date.strftime('%Y-%m-%d %H:%M:%S')},123 - INFO - Log antiguo que debe eliminarse\n")
        temp_file.write(f"{recent_date.strftime('%Y-%m-%d %H:%M:%S')},456 - INFO - Log reciente que debe mantenerse\n")
        temp_file.write(f"{current_date.strftime('%Y-%m-%d %H:%M:%S')},789 - INFO - Log actual que debe mantenerse\n")
    
    try:
        # Ejecutar la función de limpieza
        _clean_old_records_from_file(temp_path, current_date)
        
        # Leer el archivo procesado
        with open(temp_path, 'r') as f:
            content = f.read()
        
        # Verificar que solo se mantuvieron los logs recientes
        assert "Log antiguo que debe eliminarse" not in content
        assert "Log reciente que debe mantenerse" in content
        assert "Log actual que debe mantenerse" in content
        
    finally:
        # Limpiar el archivo temporal
        if os.path.exists(temp_path):
            os.unlink(temp_path)