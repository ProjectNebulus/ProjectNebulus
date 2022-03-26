from flask import Blueprint

api_blueprint = Blueprint(
    "api",
    __name__,
    url_prefix="/api",
    template_folder="templates",
    static_folder="static",
)

from . import v1
from . import developers
from .graphql import *
