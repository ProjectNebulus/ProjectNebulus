from app.routes.main import private_endpoint
from app.static.python.mongodb import create

from .. import internal


@internal.route("/create/nebulusdoc", methods=["POST"])
@private_endpoint
def newNebulusdoc():
    data = {
        "title": "Untitled Document",
        "content": """
        <font face="Montserrat" color="#a3a3a3"><b style="">Type / to insert</b></font>
        """,
    }
    id = create.create_nebulus_doc(data)
    return str(id)  # /docs/document/"
