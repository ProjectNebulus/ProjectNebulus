from flask import request, session

from app.static.python.mongodb import update
from .. import internal


@internal.route("/update/notepad", methods=["POST"])
def update_notepad():
    course_id = request.form.get("course_id")
    content = request.form.get("content")
    return update.change_user_notepad(course_id, content, session["id"])
