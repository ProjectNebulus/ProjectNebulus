"""Check folder or document"""

from .....static.python.mongodb import read
from ....main.utils import private_endpoint
from . import internal


@internal.route("/connect-type/<id>", methods=["POST"])
@private_endpoint
def connect_schoology_route(id):
    type = read.check_type(id)
    return type
