import datetime
from datetime import datetime

from flask import request, session

from app.static.python.classes import Avatar, ChatProfile
from app.static.python.mongodb import create
from app.static.python.utils.security import hash256
from .. import internal


@internal.route("/create/user", methods=["POST"])
def create_user():
    data = request.get_json()
    cats = ['black_cat.png', 'blue_cat.png', 'green_cat.png', 'pink_cat.png', 'yellow_cat.png', 'blurple_cat.png',
            'red_cat.png', '100_cat.png', 'river_cat.png', 'cake_cat.png', 'ocean_cat.png', 'mountains.png',
            'pizza.png', 'popTart.png', 'v3.gif', 'v2.gif', 'newBlue.png', 'newGreen.png', 'newJade.png', 'newPink.png',
            'newRed.png', 'newYellow.png', 'ukraine.png', 'pride.png']

    data["avatar"] = cats[int(data["avatar"].replace("cat", ""))]
    data["avatar"] = Avatar(
        avatar_url="https://beta.nebulus.ml/static/images/nebulusCats/"
                   + data["avatar"],
        parent="User",
    )
    data["age"] = datetime.strptime(data["age"].strip(), "%m/%d/%Y")
    data["chatProfile"] = ChatProfile()
    data["password"] = str(hash256(data["password"]))
    validation = create.create_user(data)
    if validation[0] == "0":
        session["username"] = validation[1].username
        session["email"] = validation[1].email
        session["pswLen"] = len(data.get("password"))
        session["id"] = validation[1].id
        session["avatar"] = (
            data["avatar"]
            .avatar_url.replace("https://localhost:8080", "")
            .replace("https://beta.nebulus.ml", "")
        )

    return validation[0]
