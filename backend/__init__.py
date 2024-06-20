__version__ = "0.1.0"

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask, send_from_directory
import random
import os

app = Flask(__name__)

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))