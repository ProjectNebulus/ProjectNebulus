from flask import request, session

from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint
from app.static.python.mongodb import create


@internal.route("/nebulusDocuments/create", methods=["POST"])
@private_endpoint
def getDocs():
    create.createNebulusDocument(request.get_json(), session["id"])
    return "success"
