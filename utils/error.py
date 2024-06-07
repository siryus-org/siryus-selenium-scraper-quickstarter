

# Load environment variables from .env file
import os
from dotenv import load_dotenv


load_dotenv()

# Get environment variables
stage = os.getenv("STAGE")


class messageError(Exception):
    def __init__(self, message):
        if stage != 'production':
            print(message)
        super().__init__(message)
