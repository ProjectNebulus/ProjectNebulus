import flask

courses = flask.Blueprint(
    "courses",
    __name__,
    url_prefix="/courses",
    static_folder="static",
    template_folder="templates",
)
from .course import *
