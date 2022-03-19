from . import internal
from .....utils.private_endpoint import private_endpoint


@internal.route("/create-schoology-course")
@private_endpoint
def import_schoology():
    return "success"
