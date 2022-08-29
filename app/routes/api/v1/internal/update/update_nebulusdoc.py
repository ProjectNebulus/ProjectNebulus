from datetime import datetime

from flask import request

from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint
from app.static.python.mongodb import create


@internal.route("/update/nebulusdoc", methods=["POST"])
@private_endpoint
def update_nebulusdoc():
    data1 = request.form.get("title")
    data2 = request.form.get("content")
    data3 = request.form.get("id")
    data = {"title": data1, "content": data2, "id": data3}
    data["lastEdited"] = datetime.datetime.now()
    print(data)
    create.update_nebulusdoc(data)

    return "success"
