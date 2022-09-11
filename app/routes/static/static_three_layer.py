from pathlib import Path

from flask import send_from_directory

from . import static_blueprint


@static_blueprint.route("/<folder>/<folder2>/<folder3>/<file>")
def static_3layer(folder, folder2, folder3, file):
    current_dir = Path(__file__)
    root_path = [p for p in current_dir.parents if "ProjectNebulus" in p.parts[-1] ][0]
    return send_from_directory(
        f"{root_path}/app/static/{folder}/{folder2}/{folder3}", file
    )
