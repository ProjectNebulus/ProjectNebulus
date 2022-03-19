from .__init__ import internal
from .private_endpoint import private_endpoint
from .....static.python.mongodb.read import username_exists


@internal.route("/username-exists", methods=["POST"])
@private_endpoint
def email_exists():
