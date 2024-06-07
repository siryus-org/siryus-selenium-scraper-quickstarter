# Imports from external libraries
from dotenv import load_dotenv
import os
import ssl
# Flask imports and their extensions
from flask import Flask, render_template
# Imports of own modules
from controller.controller_sample import controller_sample
from utils.handle_request import handle_request_endpoint

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Get environment variables
stage = os.getenv("STAGE")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sample', methods=['GET'])
def sample_endpoint():
    return handle_request_endpoint(controller_sample)

# Add more endpoint


if __name__ == "__main__":
    if stage == "production":
        # You can change that using nginx and Gunicorn
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain("./certs/cert.pem", "./certs/private.pem")
        app.run(debug=False, host='0.0.0.0', port=3000, ssl_context=context)
    else:
        app.run(debug=True, host='0.0.0.0', port=3000)
