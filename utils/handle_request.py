import logging
import time
from flask import jsonify, request
from utils.config import DOWNLOAD_DIR, STAGE
from utils.file_manager import create_download_directory
from utils.logging_config import configure_logger
from utils.security import authenticate_token


def handle_request_endpoint(controller_function, decode_response=True):
    configure_logger()
    create_download_directory(DOWNLOAD_DIR)
    start_time = time.time()
    logging.info("|| Controller:" + controller_function.__name__)
    if not authenticate_token():
        return jsonify({"status": "ERROR", "message": "Unauthorized", "time": time.time() - start_time}), 401
    if not request.is_json:
        return jsonify({"status": "ERROR", "message": "A JSON was expected in the request body", "time": time.time() - start_time}), 400
    try:
        data = request.json
        logging.info(
            {key: value for key, value in data.items() if key != 'password'})
        message = controller_function(data)
        if decode_response:
            logging.info(f"OK - message: {message}")
            return jsonify({"status": "OK", "message": message, "time": time.time() - start_time}), 200
        else:
            return message
    except Exception as e:
        error_message = str(e)
        logging.error(f"ERROR: {error_message}")
        return jsonify({"status": "ERROR", "message": "An internal error has occurred. " + error_message, "time": time.time() - start_time}), 400
