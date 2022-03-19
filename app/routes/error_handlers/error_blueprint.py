from flask import Blueprint

error_blueprint = Blueprint(
    "error_blueprint", __name__, template_folder="/app/templates/errors"
)
