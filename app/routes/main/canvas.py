from flask import render_template, session, request

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read
import schoolopy
from ...static.python.canvas import *


@main_blueprint.route("/canvas", methods=["GET"])
@logged_in
def canvasConnect():
    # Open OAuth authorization webpage. Give time to authorize.
    return render_template("connectCanvas.html")


@main_blueprint.route("/canvas", methods=["POST"])
@logged_in
def canvasConnect2():
    a = connectCanvas(request.form.get("link"), request.form.get("key"))
    if a != False:
        session["canvas"] = str(a)
        session["canvas_key"] = request.form.get("key")
        session["canvas_link"] = request.form.get("link")
    return "<script>window.close();</script>"
