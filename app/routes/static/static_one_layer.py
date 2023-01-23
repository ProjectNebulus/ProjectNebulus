from pathlib import Path

from flask import send_file

from . import static_blueprint


@static_blueprint.route("/<folder>/<file>")
def static_1layer(folder, file):
    current_dir = Path(__file__)
    root_path = next(p for p in current_dir.parents if "ProjectNebulus" in p.parts[-1])
    return send_file(f"{root_path}/app/static/{folder}/{file}")
