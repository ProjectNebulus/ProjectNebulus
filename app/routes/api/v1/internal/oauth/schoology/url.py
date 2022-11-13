from flask import request

from app.routes.main.utils import private_endpoint
from app.static.python.extensions.integrations.schoology import generate_schoology_url
from ... import internal


@internal.route("/oauth/schoology/url", methods=["GET"])
@private_endpoint
def schoology_url():
    return generate_schoology_url(request.url_root)
