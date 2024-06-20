__version__ = "0.1.0"

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask, send_from_directory
import random
import os

from backend.endpoints import frontend_handler

app = Flask(__name__)

app.register_blueprint(frontend_handler.bp)

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))