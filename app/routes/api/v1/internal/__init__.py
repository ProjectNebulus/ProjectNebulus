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

from .check_signin import *
from .connect_to_schoology import *
from .connected_to_schoology import *
from .create_course import *
from .create_schoology_course import *
from .email_exists import *
from .generate_schoology_oauth_url import *
from .logout_of_schoology import *
from .schoology_callback import *
from .send_email import *
from .signin_post import *
from .signup_post import *
from .spotify_status import *
from .signin_with_schoology import *
from .file_upload import *
from .file_upload_link import *
from .upload_document import *
