from flas import request

from .....static.python.mongodb import delete
from . import internal


@internal.route("/delete-course", methods=["POST"])
def delete_course():
    data = request.json()
    delete.delete_course(data["id"])
    return "success"
