import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from utils.error import messageError

# Load environment variables from .env file
load_dotenv()

# Get environment variables
stage = os.getenv("STAGE")


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
        logging.info(f"Stage: {stage}")

    except Exception as e:
        # In case of error, log the error and raise an exception
        raise messageError("Error setting up logging")


# INFO

# log.debug(msg): Used for debug messages. These messages are often useful for diagnosing problems and understanding program flow during development, but should not be present in the final version of the code in production.

# log.info(msg): Used for informational messages indicating that the program is working as expected.

# log.warning(msg): Used for warning messages that indicate situations that could lead to unexpected behavior, but are not critical errors.

# log.error(msg): Used for error messages that indicate problems that have occurred, but have not caused the program to terminate.

# log.critical(msg): Used for critical severity messages that indicate serious problems that have caused the program to terminate or require immediate action.
