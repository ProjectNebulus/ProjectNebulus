import flask
from ..__init__ import courses

course = flask.Blueprint(
    "course",
    __name__,
    url_prefix="/course/<int:course_id>",
    template_folder="templates",
    static_folder="static",
)
courses.register_blueprint(course)

from .course import *
from .announcements import *
from .documents import *
from .extensions import *
from .grades import *
from .home import *
from .info import *
from .learning import *
from .settings import *
from .textbook import *


