import logging
import time
from flask import jsonify, request
from utils.config import DOWNLOAD_DIR
from utils.file_manager import create_download_directory
from utils.security import authenticate_token


def handle_request_endpoint(controller_function, decode_response=True):
    create_download_directory(DOWNLOAD_DIR)
    start_time = time.time()
    logging.info("|| Controller:" + controller_function.__name__)
    if not authenticate_token():
        return jsonify({"status": "ERROR", "message": "Unauthorized", "time": time.time() - start_time}), 401
    if not request.is_json:
        return jsonify({"status": "ERROR", "message": "A JSON was expected in the request body", "time": time.time() - start_time}), 400
    try:
        data = request.get_json()
        logging.info(
            "Request accepted for controller %s with fields %s",
            controller_function.__name__,
            sorted(data.keys()) if isinstance(data, dict) else [],
        )
        message = controller_function(data)
        if decode_response:
            logging.info("Controller %s completed", controller_function.__name__)
            return jsonify({"status": "OK", "message": message, "time": time.time() - start_time}), 200
        else:
            return message
    except Exception as e:
        logging.exception("Controller %s failed", controller_function.__name__)
        return jsonify({"status": "ERROR", "message": "The request could not be processed.", "time": time.time() - start_time}), 400
