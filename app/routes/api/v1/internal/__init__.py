import flask

from .. import v1

internal = flask.Blueprint(
    "internal",
    __name__,
    url_prefix="/internal",
    static_folder="static",
    template_folder="templates",
)
v1.register_blueprint(internal)
