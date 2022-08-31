from flask import Blueprint

static_blueprint = Blueprint(
    "static_blueprint",
    "static",
    url_prefix="/static",
    template_folder="../templates",
    static_folder="../static",
)

from .static_four_layer import *

# Importing routes for this blueprint
from .static_one_layer import *
from .static_three_layer import *
from .static_two_layer import *
