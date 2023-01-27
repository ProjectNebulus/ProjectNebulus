from flask import request

from app.routes.main.utils import private_endpoint
from app.static.python.mongodb import update
from .. import internal

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@internal.route("/event/done", methods=["POST"])
@private_endpoint
def update_event_done():
    data = request.get_json()
    event_id = data["id"]
    update.mark_event_as_done(event_id)
    return "success"
