import logging
import os
import re
import io
import requests
import base64

from utils.error import messageError


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
    :return: Contenido binario del archivo
    :raises MessageError: Si el formato de archivo no es válido
    """
    url_pattern = re.compile(r'^https?://\S+$')

    if isinstance(data, str) and url_pattern.match(data):
        # Si es una URL, descarga el archivo
        try:
            response = requests.get(data, timeout=10)
            response.raise_for_status()  # Lanza error si el request falla
            return response.content
        except requests.RequestException as e:
            raise messageError(f"Error al descargar el archivo: {e}")

    elif isinstance(data, (bytes, io.BytesIO)):
        # Si es binario, lo devuelve tal cual
        return data if isinstance(data, bytes) else data.getvalue()

    elif isinstance(data, str):
        # Si es una cadena, se asume que es Base64 y se decodifica
        try:
            # Intentamos decodificarlo como Base64
            return base64.b64decode(data)
        except Exception as e:
            raise messageError(f"Error al decodificar Base64: {e}")

    raise messageError("Formato de archivo desconocido")
