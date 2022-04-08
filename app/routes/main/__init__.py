from flask import Blueprint

main_blueprint = Blueprint(
    "main_blueprint",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
    url_prefix="/",
)

from .about import *
from .connections import *
from .course import *
from .dashboard import *
from .home import *
from .lms import *
from .logout import *
from .points import *
from .pricing import *
from .profile import *
from .settings import *
from .signin import *
from .signup import *
from .calendar import *
from .spotify import *
from .discordauth import *
from .schoology import *
from .gclassroom import *
from .canvas import *
