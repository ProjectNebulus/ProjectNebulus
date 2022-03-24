"""Check folder or document"""

from . import internal
from ....main.utils import private_endpoint
from .....static.python.mongodb import read


@internal.route("/connect-type/<id>", methods=["POST"])
@private_endpoint
def connect_schoology(id):
    type = read.check_type(id)
    return type
