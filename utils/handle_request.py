import logging
import os
import time
from dotenv import load_dotenv
from flask import jsonify, request
from utils.logging_config import configure_logger
from utils.security import authenticate_token
# Load environment variables from .env file
load_dotenv()

# Get environment variables
stage = os.getenv("STAGE")


def handle_request_endpoint(controller_function):
    configure_logger()
    start_time = time.time()

    logging.info("|| Controller:" + controller_function.__name__)
    if stage != "production":
        print("|| Controller:" + controller_function.__name__)

    if not authenticate_token():
        return jsonify({"status": "ERROR", "message": "Unauthorized", "time": time.time() - start_time}), 401

    if not request.is_json:
        return jsonify({"status": "ERROR", "message": "A JSON was expected in the request body", "time": time.time() - start_time}), 400

    try:
        data = request.json

        logging.info(
            {key: value for key, value in data.items() if key != 'password'})
        message = controller_function(data)
        logging.info(f"OK - message: {message}")
        return jsonify({"status": "OK", "message": message, "time": time.time() - start_time}), 200

    except Exception as e:
        error_message = str(e)
        logging.error(f"ERROR: {error_message}")
        return jsonify({"status": "ERROR", "message": error_message, "time": time.time() - start_time}), 400
