from flask import Blueprint


static_blueprint = Blueprint(
    "static_blueprint",
    __name__,
    url_prefix="/static",
    template_folder="../templates",
    static_folder="../static",
)

from .folder_file import *
from .folder_folder2_file import *