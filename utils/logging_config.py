import os
import logging
from datetime import datetime
from utils.config import AUTO_DELETE_LOGS, STAGE, LOG_FILE_DELETION_DAYS
from utils.error import messageError
import re


def configure_logger():
    try:

        # Get the current date and time to use in the log file name
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Create the logs directory if it does not exist
        base_directory = '/app' if os.environ.get('DOCKERIZED', False) else ''

        logs_directory = os.path.join(base_directory, 'logs')
        os.makedirs(logs_directory, exist_ok=True)

        # Configure the name of the log file with the date, time, and incident number
        log_filename = f"{current_datetime}.log"
        log_filepath = os.path.join(logs_directory, log_filename)

        # Configure the logging system to write to the dynamically created file
        logging.basicConfig(filename=log_filepath, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Log the initiation of submission of information
        logging.info("Initiating log")
        logging.info(f"Stage: {STAGE}")

        if AUTO_DELETE_LOGS:
            delete_old_logs()

    except Exception as e:
        # In case of error, log the error and raise an exception
        raise messageError("Error setting up logging")


def delete_old_logs():
    """
    Elimina archivos de log antiguos y registros antiguos de archivos que sobreviven.
    
    Proceso:
    1. Elimina archivos completos que tengan más de LOG_FILE_DELETION_DAYS días
    2. De los archivos que sobreviven, elimina registros que tengan más de LOG_FILE_DELETION_DAYS días
    """
    try:
        current_datetime = datetime.now()
        base_directory = '/app' if os.environ.get('DOCKERIZED', False) else ''
        logs_directory = os.path.join(base_directory, 'logs')
        os.makedirs(logs_directory, exist_ok=True)

        files = os.listdir(logs_directory)
        surviving_files = []

        # Paso 1: Eliminar archivos completos antiguos (más de LOG_FILE_DELETION_DAYS días)
        for file in files:
            # Check if the filename matches the expected format (e.g., '2025-02-26_11-13-20.log')
            match = re.match(
                r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.log", file)
            if match:
                file_datetime = datetime.strptime(
                    match.group(1), "%Y-%m-%d_%H-%M-%S")
                difference = current_datetime - file_datetime

                if difference.days > LOG_FILE_DELETION_DAYS:
                    file_path = os.path.join(logs_directory, file)
                    os.remove(file_path)
                    logging.info(f"Deleted old log file: {file}")
                else:
                    surviving_files.append(file)
            else:
                # Log or handle any files that don't match the expected pattern
                logging.warning(f"Skipping file with invalid format: {file}")

        # Paso 2: Limpiar registros antiguos de archivos que sobreviven
        for file in surviving_files:
            file_path = os.path.join(logs_directory, file)
            _clean_old_records_from_file(file_path, current_datetime)

    except Exception as e:
        raise messageError("Error deleting old logs")


def _clean_old_records_from_file(file_path, current_datetime):
    """
    Limpia registros antiguos (más de LOG_FILE_DELETION_DAYS días) de un archivo de log específico.
    Si el archivo quedaría vacío después de la limpieza, lo elimina completamente.
    
    Args:
        file_path (str): Ruta completa al archivo de log
        current_datetime (datetime): Fecha y hora actual para comparar
    """
    try:
        # Leer todas las líneas del archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filtrar líneas que no sean muy antiguas
        filtered_lines = []
        records_removed = 0
        
        for line in lines:
            # Extraer timestamp del registro usando regex
            # Formato esperado: "2025-09-08 12:31:19,625 - INFO - mensaje"
            timestamp_match = re.match(
                r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - ", line)
            
            if timestamp_match:
                try:
                    # Parsear la fecha del registro
                    record_datetime = datetime.strptime(
                        timestamp_match.group(1), "%Y-%m-%d %H:%M:%S")
                    
                    # Calcular diferencia en días
                    difference = current_datetime - record_datetime
                    
                    # Mantener registros de menos de LOG_FILE_DELETION_DAYS días
                    if difference.days <= LOG_FILE_DELETION_DAYS:
                        filtered_lines.append(line)
                    else:
                        records_removed += 1
                        
                except ValueError:
                    # Si hay error parseando la fecha, mantener la línea
                    filtered_lines.append(line)
            else:
                # Si no tiene formato de timestamp reconocible, mantener la línea
                filtered_lines.append(line)
        
        # Verificar si el archivo quedaría vacío o solo con líneas vacías
        content_lines = [line for line in filtered_lines if line.strip()]
        
        if not content_lines:
            # Si no hay contenido útil, eliminar el archivo completo
            os.remove(file_path)
            filename = os.path.basename(file_path)
            logging.info(f"Deleted empty log file after cleaning: {filename}")
        elif records_removed > 0:
            # Solo reescribir el archivo si se removieron registros y hay contenido
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)
            
            filename = os.path.basename(file_path)
            logging.info(f"Cleaned {records_removed} old records from {filename}")
            
    except Exception as e:
        logging.error(f"Error cleaning old records from {file_path}: {str(e)}")
        # No lanzar excepción para no afectar el procesamiento de otros archivos


# INFO

# log.debug(msg): Used for debug messages. These messages are often useful for diagnosing problems and understanding program flow during development, but should not be present in the final version of the code in production.

# log.info(msg): Used for informational messages indicating that the program is working as expected.

# log.warning(msg): Used for warning messages that indicate situations that could lead to unexpected behavior, but are not critical errors.

# log.error(msg): Used for error messages that indicate problems that have occurred, but have not caused the program to terminate.

# log.critical(msg): Used for critical severity messages that indicate serious problems that have caused the program to terminate or require immediate action.

# CONFIGURACIÓN DE LIMPIEZA DE LOGS:
# - AUTO_DELETE_LOGS: Si está habilitado, se ejecuta automáticamente la limpieza de logs
# - LOG_FILE_DELETION_DAYS: Número de días después de los cuales se eliminan logs y registros (configurado en config.py)
# - Archivos completos: Se eliminan archivos de log que tengan más de LOG_FILE_DELETION_DAYS días de antigüedad
# - Registros individuales: De los archivos que sobreviven, se eliminan registros más antiguos de LOG_FILE_DELETION_DAYS días
# - Archivos vacíos: Si un archivo queda sin contenido útil después de la limpieza, se elimina completamente
# - Los archivos se identifican por su formato de nombre: YYYY-MM-DD_HH-MM-SS.log
# - Los registros se identifican por su timestamp en formato: YYYY-MM-DD HH:MM:SS,milliseconds
