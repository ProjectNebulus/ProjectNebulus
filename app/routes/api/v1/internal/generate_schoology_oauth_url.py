from .....static.python.extensions.integrations.schoology import generate_schoology_url
from flask import request, session

from . import internal
from ....main.utils import private_endpoint


@internal.route("/generate-schoology-oauth-url", methods=["GET"])
@private_endpoint
def generate_url_signin():
    return generate_schoology_url(request.url_root)
