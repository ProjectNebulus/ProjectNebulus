"""Check folder or document"""

from app.routes.api.v1.internal import internal
from app.routes.main.utils import private_endpoint
from app.static.python.mongodb import read


@internal.route("/connect-type/<id>", methods=["POST"])
@private_endpoint
def connect_schoology_route(id):
    type = read.check_type(id)
    return type
