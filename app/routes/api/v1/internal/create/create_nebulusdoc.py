from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint
from app.static.python.mongodb import create


@internal.route("/create/nebulusdoc", methods=["POST"])
@private_endpoint
def newNebulusdoc():
    data = {
        "title": "Untitled Document",
        "content": """
        <font face="Montserrat" color="#a3a3a3"><b style="">Type / to insert</b></font>
        """,
    }
    id = create.create_nebulusdoc(data)
    return str(id)  # /docs/document/"
