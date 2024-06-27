

from flask import Blueprint, request


bp = Blueprint('document_handler', __name__, url_prefix="/api/lookup")

@bp.route('/embed', methods=["POST"])
def embed_document():
    request.json