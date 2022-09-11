from flask import request

from app.routes.main import private_endpoint
from .. import internal


@internal.route("/get/nebulusdoc", methods=["POST"])
@private_endpoint
def readDoc():
    the_id = request.form.get("id")
