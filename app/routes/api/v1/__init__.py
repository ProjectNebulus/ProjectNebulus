import flask
from ..__init__ import api

v1 = flask.Blueprint(
    "v1",
    __name__,
    url_prefix="/v1",
    static_folder="static",
    template_folder="templates",
)
api.register_blueprint(v1)
