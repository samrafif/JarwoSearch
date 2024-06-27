import os

from flask import (
    Blueprint, send_from_directory, url_for
)

from backend.constants import root_dir, Server

bp = Blueprint("frontend", __name__)

# Path for our main Svelte page
@bp.route("/")
def base():
    print(root_dir)

    return send_from_directory(os.path.join(root_dir, Server.frontend_entrypoint), "index.html")

# Path for all the static files (compiled JS/CSS, etc.)
@bp.route("/<path:path>")
def home(path):
    
    return send_from_directory(os.path.join(root_dir, Server.frontend_entrypoint), path)

def checks(app):
    from os.path import isdir, isfile, join

    checks = [isdir(Server.frontend_entrypoint), isfile(join(Server.frontend_entrypoint, "index.html"))]
    return all(checks)

def setup(app):
    app.register_blueprint(bp)