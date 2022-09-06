from flask import Blueprint

api_blueprint = Blueprint(
    "api",
    "api",
    url_prefix="/api",
    template_folder="templates",
    static_folder="static",
)

# Importing routes for this blueprint

from .developers import *
from .v1 import *

# from app.routes.api import graphql
