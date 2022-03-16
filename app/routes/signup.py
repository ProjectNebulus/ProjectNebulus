from app.routes import simple_page
from flask import session, render_template, redirect


@simple_page.route("/signup", methods=["GET"])
def signup():
    if session.get("username") and session.get("password"):
        return redirect("/dashboard")
    return render_template(
        "main/signup.html", page="Nebulus - Sign Up", disablebar=True
    )
