from flas import request
from . import internal
from .....static.python.mongodb import delete


@internal.route("/delete-course", methods=["POST"])
def delete_course():
    data = request.json()
    delete.delete_course(data["id"])
    return "success"
