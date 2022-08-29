from app.routes.main import private_endpoint

from app.routes.main import private_endpoint


@internal.route(
    "nebulusDocuments/share", methods=["POST"]
)  # For sharing a document with another user
@private_endpoint
def shareDoc():
    pass
