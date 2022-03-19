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
