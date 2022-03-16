from app.routes import simple_page
from flask import session, render_template, redirect


@simple_page.route("/signin", methods=["GET"])
def signin():
    if not (session.get("username") and session.get("password")):
        return render_template(
            "main/signin.html", page="Nebulus - Log In", disablebar=True
        )
    return redirect("/dashboard")
