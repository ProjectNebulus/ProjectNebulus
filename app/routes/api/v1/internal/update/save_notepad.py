from flask import request, session

from flask import request, session

from app.routes.api.v1.internal import internal
from app.static.python.mongodb import update


@internal.route("/nebulusnotepad/save", methods=["POST"])
def change_notepad():
    course_id = request.form.get("course_id")
    content = request.form.get("content")
    return update.change_user_notepad(course_id, content, session["id"])
