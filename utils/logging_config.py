import os
import logging
from datetime import datetime
from utils.config import AUTO_DELETE_LOGS, STAGE
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
    try:
        current_datetime = datetime.now()
        base_directory = '/app' if os.environ.get('DOCKERIZED', False) else ''
        logs_directory = os.path.join(base_directory, 'logs')
        os.makedirs(logs_directory, exist_ok=True)

        files = os.listdir(logs_directory)

        for file in files:
            # Check if the filename matches the expected format (e.g., '2025-02-26_11-13-20.log')
            match = re.match(
                r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.log", file)
            if match:
                file_datetime = datetime.strptime(
                    match.group(1), "%Y-%m-%d_%H-%M-%S")
                difference = current_datetime - file_datetime
                months = difference.days / 30

                if months > 1:
                    os.remove(os.path.join(logs_directory, file))
            else:
                # Log or handle any files that don't match the expected pattern
                logging.warning(f"Skipping file with invalid format: {file}")

    except Exception as e:
        raise messageError("Error deleting old logs")


# INFO

# log.debug(msg): Used for debug messages. These messages are often useful for diagnosing problems and understanding program flow during development, but should not be present in the final version of the code in production.

# log.info(msg): Used for informational messages indicating that the program is working as expected.

# log.warning(msg): Used for warning messages that indicate situations that could lead to unexpected behavior, but are not critical errors.

# log.error(msg): Used for error messages that indicate problems that have occurred, but have not caused the program to terminate.

# log.critical(msg): Used for critical severity messages that indicate serious problems that have caused the program to terminate or require immediate action.
