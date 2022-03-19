from . import main_blueprint
from flask import render_template, redirect, session, request
from ...static.python.mongodb import read
from ...utils.logged_in import logged_in


@main_blueprint.route("/lms", methods=["GET"])
@logged_in
def lms():
    new_user = request.args.get("new_user", default="false", type=str)
    user_acc = read.find_user(id=session["id"])
    user_courses = read.get_user_courses(session["id"])
    return render_template(
        "lms.html",
        password=session["password"],
        user=session["username"],
        user_acc=user_acc,
        user_courses=user_courses,
        read=read,
        page="Nebulus - Learning",
        new_account=new_user == "true",
    )
