from flask import render_template, session

from app.static.python.mongodb import read
from app.static.python.mongodb.read import get_text
from . import main_blueprint


@main_blueprint.route("/documents", methods=["GET"])
def docs():
    docs = read.get_user_docs(session["id"])
    return render_template(
        "learning/tools/docs.html",
        user=session.get("username"),
        user_id=session.get("id"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=get_text,
        docs=docs,
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
    user_notepad = read.get_user_notepad(session["id"])
    # print(user_notepad)
    # print(courses[0])
    # # print(user_notepad[courses[0].name])
    # print(user_notepad[courses[0].id])
    return render_template(
        "learning/tools/notepad.html",
        page="Nebulus - Notepad",
        user=session.get("username"),
        user_id=session.get("id"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        fonts=fonts,
        translate=get_text,
        courses=courses,
        notepad=user_notepad,
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
        document = read.get_neb_doc(id)
        print(document)
        # check authorized user

        content = document["content"]
        title = document["title"]
        return render_template(
            "learning/tools/document.html",
            page="Nebulus - Notepad",
            user=session.get("username"),
            user_id=session.get("id"),
            avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
            read=read,
            fonts=fonts,
            translate=get_text,
            content=content,
            title=title,
            id=id,
        )
    except Exception as e:
        print(e)
        return "404"
