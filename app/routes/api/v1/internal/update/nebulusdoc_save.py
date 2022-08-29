import datetime

from flask import request

from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint
from app.static.python.mongodb import read


@internal.route("nebulusDocuments/save", methods=["POST"])
@private_endpoint
def saveDoc():
    data = request.get_json()
    try:
        document = read.getDocument(data["id"])
    except KeyError:
        return "false"

    document.lastEdited = datetime.datetime.now()
    for key, value in data.items():
        document.setattr(key, value)
    document.save()
    return

