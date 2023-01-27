import flask

from .. import v1

internal = flask.Blueprint(
    "internal",
    "internal",
    url_prefix="/internal",
    static_folder="static",
    template_folder="templates",
)
v1.register_blueprint(internal)

from .check import *
from .create import *
from .delete import *
from .get import *
from .oauth import *
from .search import *
from .update import *
