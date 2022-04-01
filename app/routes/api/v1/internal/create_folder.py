from flask import request
from . import internal
from .....static.python.mongodb.create import createFolder


@internal.route('/create-folder', methods=['POST'])
def create_folder():
    createFolder(request.json())
    return 'success', 200
