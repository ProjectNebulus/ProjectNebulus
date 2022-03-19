from flask import Blueprint
from ..__init__ import main_blueprint

error_blueprint = Blueprint(
    "error_blueprint", __name__, template_folder="/app/templates/errors"
)
main_blueprint.register_blueprint(error_blueprint)
