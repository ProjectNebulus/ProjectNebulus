from flask import Blueprint, session, send_file
from app.static.python.mongodb import read as r

static_blueprint = Blueprint('static_blueprint', __name__, url_prefix="/static", template_folder="../templates",
                             static_folder="../static")


# fixed: FileNotFoundError: [Errno 2] No such file or directory: '/Users/<>/IdeaProjects/ProjectNebulus/app/routes/app/static/images/logo.png'
@static_blueprint.route("/<folder>/<file>")
def static1(folder, file):
    return send_file(f"../static/{folder}/{file}")


@static_blueprint.route("/<folder>/<folder2>/<file>")
def static2(folder, folder2, file):
    return send_file(f"../static/{folder}/{folder2}/{file}")
