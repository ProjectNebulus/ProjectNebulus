# TODO
from flask import request, session
from . import internal
from .....static.python.mongodb import read


@internal.route("/search-object", methods=["POST"])
def search_object():
    data = request.get_json()
    results = read.search(data["keyword"], session["id"])
