from app.routes.api import internal

from app.routes.main import private_endpoint


@internal.route(
    "/update/nebulusdoc/sharing", methods=["POST"]
)  # For sharing a document with another user
@private_endpoint
def share_nebulusdoc():
    pass
