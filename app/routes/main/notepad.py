from flask import render_template, session

from app.static.python.mongodb import read
from . import main_blueprint
from ...static.python.mongodb.read import getText


@main_blueprint.route("/documents", methods=["GET"])
def docs():
    return render_template(
        "tools/docs.html",
        user=session.get("username"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=getText,
    )


@main_blueprint.route("/notepad", methods=["GET"])
def notepad():
    fonts = [
        "Arial",
        "Times New Roman",
        "Comic Sans MS",
        "Pacifico",
        "Roboto",
        "Lobster",
        "Lato",
        "Montserrat",
        "Raleway",
        "Roboto Condensed",
        "Open Sans",
        "Roboto Slab",
        "Merriweather",
        "Ubuntu",
        "PT Sans",
        "PT Serif",
        "Ubuntu Condensed",
        "Droid Sans",
        "Droid Serif",
        "Roboto Mono",
        "Roboto Mono Condensed",
        "Roboto Mono Slashed",
        "Roboto Mono Slashed Condensed",
        "Roboto Mono Slashed Slashed",
        "Roboto Mono Slashed Slashed Condensed",
    ]
    courses = list(read.get_user_courses(session["id"]))
    print(courses)
    return render_template(
        "tools/notepad.html",
        page="Nebulus - Notepad",
        user=session.get("username"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        fonts=fonts,
        translate=getText,
        courses=courses,
    )


@main_blueprint.route("/docs/document/<id>", methods=["GET"])
def document(id):
    fonts = [
        "Arial",
        "Times New Roman",
        "Comic Sans MS",
        "Pacifico",
        "Roboto",
        "Lobster",
        "Lato",
        "Montserrat",
        "Raleway",
        "Roboto Condensed",
        "Open Sans",
        "Roboto Slab",
        "Merriweather",
        "Ubuntu",
        "PT Sans",
        "PT Serif",
        "Ubuntu Condensed",
        "Droid Sans",
        "Droid Serif",
        "Roboto Mono",
        "Roboto Mono Condensed",
        "Roboto Mono Slashed",
        "Roboto Mono Slashed Condensed",
        "Roboto Mono Slashed Slashed",
        "Roboto Mono Slashed Slashed Condensed",
    ]
    try:
        document = read.get_nebulusdoc(id)
        return render_template(
            "tools/notepad.html",
            page="Nebulus - Notepad",
            user=session.get("username"),
            avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
            read=read,
            fonts=fonts,
            translate=getText,
        )
    except:
        return "404"
