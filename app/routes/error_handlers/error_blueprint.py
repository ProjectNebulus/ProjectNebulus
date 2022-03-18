from flask import Blueprint

error_blueprint = Blueprint(
    "error_blueprint", __name__, template_folder="templates/errors"
)
