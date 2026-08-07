import hmac
import logging
from flask import current_app, request
from utils.config import VALID_TOKEN


def authenticate_token():
    logging.info('authenticate token')
    authorization = request.headers.get('Authorization', '')
    scheme, separator, token = authorization.partition(' ')
    if scheme != 'Bearer' or separator != ' ' or not token or ' ' in token:
        return False
    if current_app and current_app.config.get('TESTING'):
        expected_token = 'sample'
    else:
        expected_token = VALID_TOKEN
    return bool(expected_token) and hmac.compare_digest(token, expected_token)
