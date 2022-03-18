from flask import Blueprint, session, send_file
from app.static.python.mongodb import read as r

static_blueprint = Blueprint('static_blueprint', __name__, url_prefix="/static", template_folder="../templates",
                             static_folder="../static")


@static_blueprint.route("/<folder>/<file>")
def static1(folder, file):
    return send_file(f"app/static/{folder}/{file}")


@static_blueprint.route("/<folder>/<folder2>/<file>")
def static2(folder, folder2, file):
    return send_file(f"app/static/{folder}/{folder2}/{file}")
