# TODO
from flask import request, session

from app.routes.api.v1.internal import internal
from app.static.python.mongodb import read


@internal.route("/search-object", methods=["POST"])
def search_object():
    data = request.get_json()
    results = read.search(data["keyword"], session["username"])
