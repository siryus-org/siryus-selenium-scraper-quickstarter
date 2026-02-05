import logging
from flask import current_app, request
from utils.config import VALID_TOKEN


def authenticate_token():
    # Replace this with your actual token authentication logic
    logging.info('authenticate token')
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return False
    token = token.split(' ')[1]
    if current_app and current_app.config.get('TESTING'):
        return token == 'sample'
    return token == VALID_TOKEN
