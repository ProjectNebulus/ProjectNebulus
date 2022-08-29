from flask import request

from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint


@internal.route("/get/nebulusdoc", methods=["POST"])
@private_endpoint
def readDoc():
    the_id = request.form.get("id")
