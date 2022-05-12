from flask import Blueprint

main_blueprint = Blueprint(
    "main_blueprint",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
    url_prefix="/",
)

from app.routes.main.about import *
from app.routes.main.connections import *
from app.routes.main.course import *
from app.routes.main.dashboard import *
from app.routes.main.index import *
from app.routes.main.lms import *
from app.routes.main.logout import *
from app.routes.main.points import *
from app.routes.main.pricing import *
from app.routes.main.profile import *
from app.routes.main.settings import *
from app.routes.main.signin import *
from app.routes.main.signup import *
from app.routes.main.calendar import *
from app.routes.main.spotify import *
from app.routes.main.discordauth import *
from app.routes.main.schoology import *
from app.routes.main.gclassroom import *
from app.routes.main.canvas import *
from app.routes.main.chat import *