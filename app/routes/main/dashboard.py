from . import main_blueprint
from flask import render_template, session, request
from ...static.python.mongodb import read
from ...utils.logged_in import logged_in


@main_blueprint.route("/dashboard", methods=["GET"])
@logged_in
def dashboard():
    new_user = request.args.get("new_user", default="false", type=str)
    user_courses = read.get_user_courses(session.get("id"))
    return render_template(
        "dashboard.html",
        password=session["password"],
        user=session["username"],
        email=session["email"],
        user_courses=user_courses,
        read=read,
        page="Nebulus - Dashboard",
        new_account=new_user == "true",
    )
