from flask import request
from . import internal
from ....static.python.mongodb.create import createChat

@internal.route('/create-chat', methods=['POST'])
def create_chat():
    data = request.get_json()
    createChat(data)
    return 'success'

