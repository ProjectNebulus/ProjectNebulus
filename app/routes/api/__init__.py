from flask import Blueprint

api = Blueprint(
    "api",
    __name__,
    url_prefix="/api",
    template_folder="templates",
    static_folder="static",
)

from .v1 import *
from .developers import *
from .graphql import *
