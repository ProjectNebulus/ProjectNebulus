from flask import request
from . import internal
from .....static.python.mongodb.create import createDocumentFile

@internal.route('/create-document', methods=['POST'])
def create_document():
    """
    Create a new document.
    """
    createDocumentFile(request.json())
    return 'success', 200