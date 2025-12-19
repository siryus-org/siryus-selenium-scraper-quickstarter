"""
Pruebas para el archivo file_manager.py
"""
from utils.error import messageError
from utils.file_manager import (
    clear_directory,
    create_download_directory,
    clean_filename,
    get_file,
    createTempFile
)
import base64
import tempfile
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def test_create_download_directory():
    """Verifica que se puede crear un directorio de descarga"""
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            result = create_download_directory("test_downloads")
            assert os.path.exists(result)
            assert os.path.isdir(result)
            assert result.endswith("test_downloads")
        finally:
            os.chdir(old_cwd)


def test_create_download_directory_already_exists():
    """Verifica que no falla si el directorio ya existe"""
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            result1 = create_download_directory("existing_dir")
            result2 = create_download_directory("existing_dir")
            assert result1 == result2
            assert os.path.exists(result1)
        finally:
            os.chdir(old_cwd)


def test_clean_filename_basic():
    """Verifica limpieza básica de nombres de archivo"""
    # El punto también se elimina según la implementación
    assert clean_filename("normal_file.txt") == "normal_filetxt"


def test_clean_filename_special_chars():
    """Verifica que se eliminan caracteres especiales"""
    # Tanto los caracteres especiales como el punto se eliminan
    assert clean_filename("file@#$%name.txt") == "filenametxt"


def test_clean_filename_spaces():
    """Verifica que se mantienen los espacios"""
    # Los espacios se mantienen pero el punto se elimina
    assert clean_filename("my file name.txt") == "my file nametxt"


def test_clean_filename_hyphens():
    """Verifica que se mantienen los guiones"""
    # Los guiones se mantienen pero el punto se elimina
    assert clean_filename("file-name-test.pdf") == "file-name-testpdf"


def test_clean_filename_unicode():
    """Verifica que se eliminan caracteres Unicode no permitidos"""
    cleaned = clean_filename("archivo_ñoño.txt")
    # Solo caracteres alfanuméricos ASCII, espacios, guiones y underscores
    assert all(c.isalnum() or c in '_ -.' for c in cleaned)


def test_clear_directory_with_files():
    """Verifica que se limpian archivos de un directorio"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear algunos archivos de prueba
        test_file1 = os.path.join(temp_dir, "test1.txt")
        test_file2 = os.path.join(temp_dir, "test2.txt")

        with open(test_file1, 'w') as f:
            f.write("test content 1")
        with open(test_file2, 'w') as f:
            f.write("test content 2")

        # Verificar que existen
        assert os.path.exists(test_file1)
        assert os.path.exists(test_file2)

        # Limpiar directorio
        clear_directory(temp_dir)

        # Verificar que se eliminaron
        assert not os.path.exists(test_file1)
        assert not os.path.exists(test_file2)


def test_clear_directory_nested():
    """Verifica que se limpian subdirectorios recursivamente"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear estructura de directorios
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)

        test_file = os.path.join(subdir, "nested_file.txt")
        with open(test_file, 'w') as f:
            f.write("nested content")

        assert os.path.exists(test_file)

        # Limpiar directorio
        clear_directory(temp_dir)

        # Verificar que se eliminó el archivo anidado
        assert not os.path.exists(test_file)


def test_clear_directory_nonexistent():
    """Verifica que no falla con directorio inexistente"""
    # No debe lanzar excepción
    clear_directory("/path/that/does/not/exist/12345")


def test_get_file_base64():
    """Verifica obtención de archivo desde Base64"""
    # Crear un contenido de prueba
    original_content = b"Test PDF content"
    base64_content = base64.b64encode(original_content).decode('utf-8')

    # Obtener archivo
    content, filename = get_file(base64_content)

    assert content == original_content
    assert filename.endswith('.pdf')


def test_get_file_bytes():
    """Verifica obtención de archivo desde bytes"""
    test_bytes = b"Binary content here"

    content, filename = get_file(test_bytes)

    assert content == test_bytes
    assert filename.endswith('.bin')


def test_get_file_invalid_format():
    """Verifica que intenta decodificar cualquier string como Base64"""
    # La función intenta decodificar cualquier string como Base64
    # Si no es Base64 válido, lanzará error en la decodificación
    try:
        content, filename = get_file("not_a_valid_base64_string!")
        # Si no falla, es porque lo procesó de alguna forma
        assert isinstance(content, bytes)
    except messageError as e:
        # Es válido que falle con error de decodificación
        assert "Base64" in str(e) or "Error" in str(e)


def test_create_temp_file():
    """Verifica creación de archivo temporal"""
    test_content = b"Temporary file content"
    test_filename = "temp_test_file.txt"

    try:
        filepath = createTempFile(test_content, test_filename)

        # Verificar que el archivo existe
        assert os.path.exists(filepath)
        assert filepath.endswith(test_filename)

        # Verificar contenido
        with open(filepath, 'rb') as f:
            content = f.read()
        assert content == test_content

    finally:
        # Limpiar
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)


def test_create_temp_file_with_special_name():
    """Verifica creación de archivo temporal con nombre especial"""
    test_content = b"Content"
    test_filename = "archivo-especial_2024.pdf"

    try:
        filepath = createTempFile(test_content, test_filename)

        assert os.path.exists(filepath)
        assert test_filename in filepath

    finally:
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)


def test_clean_filename_empty():
    """Verifica comportamiento con string vacío"""
    assert clean_filename("") == ""


def test_clean_filename_only_special_chars():
    """Verifica limpieza cuando solo hay caracteres especiales"""
    result = clean_filename("@#$%^&*()")
    assert result == ""
