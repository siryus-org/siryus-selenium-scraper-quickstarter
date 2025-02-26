
from utils.config import STAGE


class messageError(Exception):
    def __init__(self, message):
        if STAGE != 'production':
            print(message)
        super().__init__(message)
