import uuid
from datetime import datetime, timezone
import os

from flask import Blueprint, request, jsonify, redirect, send_from_directory
from werkzeug.utils import secure_filename

from backend.document_handler.converter import extract_files
from backend.constants import DocumentHandler, root_dir
from backend.database.models import Document
from backend.database import db

bp = Blueprint('document_handler', __name__, url_prefix="/api/docs")
upload_path = DocumentHandler.upload_folder

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in DocumentHandler.converted_types + \
                DocumentHandler.unconverted_types

@bp.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist("file")
    print(files)

    if len(files) == 0:
        return jsonify({"message":"No files attached"}), 400

    filenames = []
    for file in files:
        filename = secure_filename(file.filename)
        filenames.append(filename)
        file.save(os.path.join(upload_path, filename))

        id = str(uuid.uuid4())
        time_date_rn = datetime.now(timezone.utc).strftime("%d%m%Y_%H%M%S")
        new_doc = Document(id, filename, time_date_rn, False)
        db.session.add(new_doc)
        db.session.commit()

    extract_files(filenames)

    return jsonify({"message":"success"}), 200

@bp.route('/<path:filename>', methods=['GET','POST', 'DELETE'])
def index(filename):
    print(filename)

    # TODO: UPDATE TO ^3.10 and change to use switch/case
    if request.method == 'GET':
        return send_from_directory(os.path.join(root_dir, upload_path), filename)

def checks(app):
    import os

    checks = [os.path.isfile(DocumentHandler.tesseract_binary)]
    return all(checks)

def setup(app):
    app.register_blueprint(bp)