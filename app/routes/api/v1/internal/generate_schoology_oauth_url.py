from flask import request

from .....static.python.extensions.integrations.schoology import generate_schoology_url
from ....main.utils import private_endpoint
from . import internal


@internal.route("/generate-schoology-oauth-url", methods=["GET"])
@private_endpoint
def generate_url_signin():
    return generate_schoology_url(request.url_root)
