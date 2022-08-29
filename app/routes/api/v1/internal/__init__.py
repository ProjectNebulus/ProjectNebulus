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

from app.routes.api.v1.internal.check.account.check_signin import *
from app.routes.api.v1.internal.check.account.check_signup_email import *
from app.routes.api.v1.internal.check.account.check_signup_user import *
from app.routes.api.v1.internal.check.account.check_verification_code import *
from app.routes.api.v1.internal.check.account.email_exists import *
from app.routes.api.v1.internal.check.account.signin_post import *
from app.routes.api.v1.internal.check.account.signup_post import *
from app.routes.api.v1.internal.check.account.username_exists import *
from app.routes.api.v1.internal.check.schoology.schoology import *
