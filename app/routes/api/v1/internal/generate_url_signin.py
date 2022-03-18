from flask import Blueprint, request, jsonify
from .__init__ import internal

generate_url_signin = Blueprint(
    "generate_url_signin",
    __name__,
    url_prefix="/generate_url_signin",
    static_folder="static",
    template_folder="templates",
)
internal.register_blueprint(generate_url_signin)
