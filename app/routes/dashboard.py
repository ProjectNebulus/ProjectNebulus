from app.routes.main_blueprint import main_blueprint, logged_in
from flask import render_template, redirect, session, request
from app.static.python.mongodb import read


@main_blueprint.route("/dashboard", methods=["GET"])
def dashboard():
    if not logged_in():
        return redirect("/")
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
