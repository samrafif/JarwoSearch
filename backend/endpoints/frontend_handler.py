import os

from flask import (
    Blueprint, send_from_directory, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Path for our main Svelte page
@bp.route("/")
def base():
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'frontend', 'public'), 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@bp.route("/<path:path>")
def home(path):
    root_dir = os.getcwd()
    print(path)
    return send_from_directory(os.path.join(root_dir, 'frontend/public'), path)