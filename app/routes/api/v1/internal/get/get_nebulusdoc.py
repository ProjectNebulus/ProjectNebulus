from flask import request

from .. import internal
from app.routes.main import private_endpoint


@internal.route("/get/nebulusdoc", methods=["POST"])
@private_endpoint
def readDoc():
    the_id = request.form.get("id")
