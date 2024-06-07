import logging
from dotenv import load_dotenv
from flask import request
import os
load_dotenv()
stage = os.getenv("STAGE")
VALID_TOKEN = os.getenv("VALID_TOKEN")


def authenticate_token():
    # Replace this with your actual token authentication logic
    logging.info('authenticate token')
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return False
    token = token.split(' ')[1]
    return token == VALID_TOKEN
