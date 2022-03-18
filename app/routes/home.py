from app.routes import simple_page
from flask import session, render_template, redirect


def route():
    @simple_page.route("/", methods=["GET"])
    def index():
        return render_template("main/index.html", page="Nebulus - Learning, All In One")
