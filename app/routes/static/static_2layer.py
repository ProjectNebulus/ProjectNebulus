from flask import send_file
from . import static_blueprint


@static_blueprint.route("/<folder>/<folder2>/<file>")
def static_2layer(folder, folder2, file):
    return send_file(f"../static/{folder}/{folder2}/{file}")
