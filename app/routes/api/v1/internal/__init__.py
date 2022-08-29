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
from app.routes.api.v1.internal.check.account.check_signin import *
from app.routes.api.v1.internal.check.account.check_signup import *
from app.routes.api.v1.internal.check.account.check_type import *
from app.routes.api.v1.internal.check.account.check_verification_code import *
from app.routes.api.v1.internal.update.connect_to_schoology import *
from app.routes.api.v1.internal.check.connected_to_schoology import *
from app.routes.api.v1.internal.create.create_avatar import *
from app.routes.api.v1.internal.create.create_chat import *
from app.routes.api.v1.internal.create.create_course import *
from app.routes.api.v1.internal.create.create_course_resource import *
from app.routes.api.v1.internal.create.create_integration import *
from app.routes.api.v1.internal.create.create_schoology_course import *
from app.routes.api.v1.internal.create.create_user import *
from app.routes.api.v1.internal.delete.delete_course import *
from app.routes.api.v1.internal.delete.delete_user import *
from app.routes.api.v1.internal.check.email_exists import *
from app.routes.api.v1.internal.create.file_upload import *
from app.routes.api.v1.internal.create.file_upload_link import *
from app.routes.api.v1.internal.get.find_folders import *
from app.routes.api.v1.internal.get.generate_schoology_oauth_url import *
from .get_schoology_messages import *
from .logout_of_schoology import *
from app.routes.api.v1.internal.update.nebulusdoc_save import *
from app.routes.api.v1.internal.get.plagarism import *
from app.routes.api.v1.internal.update.save_config_planner import *
from .schoology_callback import *
from app.routes.api.v1.internal.search.search import *
from app.routes.api.v1.internal.create.send_email import *
from app.routes.api.v1.internal.check.account.signin_post import *
from app.routes.api.v1.internal.check.account.signup_post import *
from app.routes.api.v1.internal.get.spotify_status import *
from app.routes.api.v1.internal.create.upload_document import *
from app.routes.api.v1.internal.check.account.username_exists import *
