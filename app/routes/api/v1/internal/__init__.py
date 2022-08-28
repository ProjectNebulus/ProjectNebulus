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

# Importing routes for this blueprint

from app.routes.api.v1.internal.update.change_course import *
from .chat_functions import *
from app.routes.api.v1.internal.check.check_signin import *
from app.routes.api.v1.internal.check.check_signup import *
from app.routes.api.v1.internal.check.check_type import *
from app.routes.api.v1.internal.check.check_verification_code import *
from .connect_to_schoology import *
from .connected_to_schoology import *
from app.routes.api.v1.internal.create.create_avatar import *
from app.routes.api.v1.internal.create.create_chat import *
from app.routes.api.v1.internal.create.create_course import *
from app.routes.api.v1.internal.create.create_course_resource import *
from app.routes.api.v1.internal.create.create_integration import *
from app.routes.api.v1.internal.create.create_schoology_course import *
from app.routes.api.v1.internal.create.create_user import *
from app.routes.api.v1.internal.delete.delete_course import *
from app.routes.api.v1.internal.delete.delete_user import *
from .email_exists import *
from .file_upload import *
from .file_upload_link import *
from .find_folders import *
from .generate_schoology_oauth_url import *
from .get_schoology_messages import *
from .logout_of_schoology import *
from .nebulusdocs import *
from .plagarism import *
from .planner import *
from .schoology_callback import *
from .search import *
from .send_email import *
from app.routes.api.v1.internal.check.signin_post import *
from app.routes.api.v1.internal.check.signup_post import *
from .spotify_status import *
from .upload_document import *
from app.routes.api.v1.internal.check.username_exists import *
