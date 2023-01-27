from flask import redirect, render_template, request, session

from app.static.python.extensions.integrations.canvas import connectCanvas
from app.static.python.mongodb.read import get_text
from app.static.python.mongodb.update import canvasLogin
from . import main_blueprint
from .utils import logged_in


@main_blueprint.route("/canvas", methods=["GET"])
@logged_in
def canvasConnect():
    # Open OAuth authorization webpage. Give time to authorize.
    return render_template("user/connections/connectCanvas.html", translate=get_text)


@main_blueprint.route("/canvas", methods=["POST"])
@logged_in
def canvasConnect2():
    a = connectCanvas(request.form.get("link"), request.form.get("key"))
    if a != False:
        canvasLogin(
            session["id"],
            {
                "url": request.form.get("link"),
                "key": request.form.get("key"),
                "name": str(a),
            },
        )

    else:
        return redirect("/canvas")
    return render_template(
        "user/connections/connectCanvas.html", done=str(a), avatar=a.avatar_url
    )
