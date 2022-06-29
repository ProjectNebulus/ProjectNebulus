from flask import Blueprint

api_blueprint = Blueprint(
    "api",
    __name__,
    url_prefix="/api",
    template_folder="templates",
    static_folder="static",
)


# from app.routes.api import graphql
