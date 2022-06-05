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

from app.routes.api.v1.internal.check_signin import *
from app.routes.api.v1.internal.connect_to_schoology import *
from app.routes.api.v1.internal.connected_to_schoology import *
from app.routes.api.v1.internal.create_course import *
from app.routes.api.v1.internal.email_exists import *
from app.routes.api.v1.internal.username_exists import *
from app.routes.api.v1.internal.generate_schoology_oauth_url import *
from app.routes.api.v1.internal.logout_of_schoology import *
from app.routes.api.v1.internal.schoology_callback import *
from app.routes.api.v1.internal.send_email import *
from app.routes.api.v1.internal.signup_post import *
from app.routes.api.v1.internal.signin_post import *
from app.routes.api.v1.internal.spotify_status import *
from app.routes.api.v1.internal.signin_with_schoology import *
from app.routes.api.v1.internal.create_course_resource import *
from app.routes.api.v1.internal.file_upload import *
from app.routes.api.v1.internal.file_upload_link import *
from app.routes.api.v1.internal.upload_document import *
from app.routes.api.v1.internal.get_verification_code import *
from app.routes.api.v1.internal.create_user import *
from app.routes.api.v1.internal.check_signup import *
from app.routes.api.v1.internal.get_schoology_messages import *
from app.routes.api.v1.internal.plagarism import *
