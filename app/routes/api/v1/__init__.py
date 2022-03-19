import flask
from .. import api_blueprint

v1 = flask.Blueprint(
    "v1",
    __name__,
    url_prefix="/v1",
    static_folder="static",
    template_folder="templates",
)
print(v1.url_prefix)
api_blueprint.register_blueprint(v1)

from . import internal
