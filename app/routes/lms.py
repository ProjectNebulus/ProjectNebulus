from app.routes.main_blueprint import main_blueprint, logged_in
from flask import render_template, redirect, session, request
from app.static.python.mongodb import read


@main_blueprint.route("/lms", methods=["GET"])
def lms():
    if not logged_in():
        return redirect("/")
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
