from json import loads

from flask import request, session

from . import internal
from .....routes.main import private_endpoint
from .....static.python.mongodb import update, read, create


@internal.route("/nebulusDocuments/create", methods=["POST"])
@private_endpoint
def getDocs():
    create.createNebulusDocument(request.get_json())
    return "success"


@internal.route("nebulusDocuments/save", methods=["POST"])
@private_endpoint
def saveDoc():
    the_id = request.form.get("id")
    return


@internal.route("nebulusDocuments/read", methods=["POST"])
@private_endpoint
def readDoc():
    the_id = request.form.get("id")
