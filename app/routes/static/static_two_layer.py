from pathlib import Path

from flask import send_from_directory

# import the blueprint
from . import static_blueprint


# define the route
@static_blueprint.route("/<folder>/<folder2>/<file>")
def static_2layer(folder, folder2, file):
    # get the current directory and the root path of the project
    current_dir = Path(__file__)
    root_path = next(p for p in current_dir.parents if "ProjectNebulus" in p.parts[-1])

    # return the file from the specified directory
    return send_from_directory(f"{root_path}/app/static/{folder}/{folder2}", file)
