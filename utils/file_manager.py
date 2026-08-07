import logging
import os
import re
import io
import ipaddress
import requests
import base64
import socket
from urllib.parse import urljoin, urlsplit

from utils.config import MAX_DOWNLOAD_BYTES
from utils.error import messageError
import uuid
import tempfile
import shutil
from datetime import datetime


_REDIRECT_CODES = {301, 302, 303, 307, 308}


def _validate_public_url(url):
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise messageError("La URL de descarga no es válida")
    if parsed.username or parsed.password:
        raise messageError("La URL de descarga no puede contener credenciales")
    try:
        addresses = {
            result[4][0]
            for result in socket.getaddrinfo(
                parsed.hostname,
                parsed.port or (443 if parsed.scheme == "https" else 80),
            )
        }
    except socket.gaierror as error:
        raise messageError("No se pudo resolver el servidor de descarga") from error
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise messageError("No se permiten descargas desde redes privadas o locales")


def _download_public_url(url):
    current_url = url
    for _ in range(6):
        _validate_public_url(current_url)
        response = requests.get(
            current_url,
            timeout=10,
            allow_redirects=False,
            stream=True,
        )
        if response.status_code in _REDIRECT_CODES:
            location = response.headers.get("Location")
            response.close()
            if not location:
                raise messageError("La redirección de descarga no contiene destino")
            current_url = urljoin(current_url, location)
            continue
        response.raise_for_status()
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_DOWNLOAD_BYTES:
            response.close()
            raise messageError("El archivo supera el tamaño máximo permitido")
        content = bytearray()
        for chunk in response.iter_content(chunk_size=64 * 1024):
            content.extend(chunk)
            if len(content) > MAX_DOWNLOAD_BYTES:
                response.close()
                raise messageError("El archivo supera el tamaño máximo permitido")
        response.close()
        return bytes(content), current_url
    raise messageError("La descarga contiene demasiadas redirecciones")


def clear_directory(directory):
    # Check if the directory exists
    if os.path.exists(directory):
        # Iterate over files in directory
        for file_name in os.listdir(directory):
            # Create the full path to the file
            file_path = os.path.join(directory, file_name)
            try:
                # Check if the item is a file
                if os.path.isfile(file_path):
                    # Delete the file
                    os.remove(file_path)
                # If it is a directory, recursively delete its contents
                elif os.path.isdir(file_path):
                    clear_directory(file_path)
            except Exception as e:
                logging.info(f"Could not delete {file_path}: {e}")
    else:
        logging.info(f"The directory {directory} does not exist")


def create_download_directory(directory_name):

    # Creates a directory for downloading files within the current working directory.

    # Args:
    #     directory_name (str): Name of the directory to be created.

    current_directory = os.getcwd()
    download_dir = os.path.join(current_directory, directory_name)
    os.makedirs(download_dir, exist_ok=True)
    return download_dir


def clean_filename(filename):
    # Defines a regular expression that matches any character that is not a letter, number, space, or underscore
    invalid_chars_regex = r'[^\w\s-]'
    # Replaces invalid characters with an empty string
    cleaned_filename = re.sub(invalid_chars_regex, '', filename)
    return cleaned_filename


def get_file(data):
    """ 
    Obtiene el contenido de un archivo, ya sea desde una URL, un binario o en Base64.

    :param data: URL del archivo, contenido binario o cadena Base64
    :return: Contenido binario del archivo, nombre del archivo y su extensión
    :raises MessageError: Si el formato de archivo no es válido
    """
    url_pattern = re.compile(r'^https?://\S+$')

    if isinstance(data, str) and url_pattern.match(data):
        # Si es una URL, obtiene el nombre y extensión del archivo
        try:
            content, final_url = _download_public_url(data)

            # Obtener el nombre y la extensión desde la URL
            file_name = os.path.basename(urlsplit(final_url).path)
            if not file_name:  # Si no se obtiene el nombre del archivo, genera un ID único
                file_name = f"{uuid.uuid4()}.unknown"

            return content, file_name

        except (requests.RequestException, ValueError) as e:
            raise messageError(f"Error al descargar el archivo: {e}")

    elif isinstance(data, (bytes, io.BytesIO)):
        # Si es binario, lo devuelve tal cual
        # Genera un nombre genérico para binarios
        file_name = f"{uuid.uuid4()}.bin"
        return data if isinstance(data, bytes) else data.getvalue(), file_name

    elif isinstance(data, str):
        # Si es una cadena, se asume que es Base64 y se decodifica
        try:
            # Intentamos decodificarlo como Base64
            decoded_data = base64.b64decode(data, validate=True)
            if len(decoded_data) > MAX_DOWNLOAD_BYTES:
                raise messageError("El archivo supera el tamaño máximo permitido")
            file_name = f"{uuid.uuid4()}.pdf"  # Nombre genérico para Base64
            return decoded_data, file_name
        except Exception as e:
            raise messageError(f"Error al decodificar Base64: {e}")

    raise messageError("Formato de archivo desconocido")


def createTempFile(data, file_name):
    safe_file_name = os.path.basename(file_name)
    if safe_file_name != file_name or safe_file_name in {"", ".", ".."}:
        raise messageError("Nombre de archivo no válido")
    # Crear el archivo temporal con delete=False
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Escribir los datos en el archivo temporal
        temp_file.write(data)
        temp_file_path = temp_file.name

    # Renombrar el archivo temporal con el nombre especificado
    final_path = os.path.join(os.path.dirname(temp_file_path), safe_file_name)
    # Mover y renombrar el archivo temporal
    shutil.move(temp_file_path, final_path)

    # Retorna la ruta del archivo renombrado
    return final_path

def take_screenshot(driver, directory="logs"):
    """
    Toma una captura de pantalla del navegador y la guarda con la fecha y hora actual.

    Args:
        driver: Instancia del WebDriver de Selenium
        directory (str): Directorio donde guardar la captura (por defecto "logs")

    Returns:
        str: Ruta completa del archivo de captura guardado
    """
    try:
        # Crear directorio si no existe
        os.makedirs(directory, exist_ok=True)

        # Generar nombre del archivo con fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(directory, filename)

        # Tomar captura de pantalla
        driver.save_screenshot(filepath)

        logging.info(f"Screenshot saved: {filepath}")
        return filepath

    except Exception as e:
        logging.error(f"Error taking screenshot: {e}")
        raise messageError(f"Error al tomar captura de pantalla: {e}")
