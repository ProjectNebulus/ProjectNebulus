from flask import request, flash
from . import internal
from .....static.python.plagarism import daplagarism


@internal.route("/plagarism", methods=["POST"])
def plagarism():
    """
    Json input:

    """
    data = request.form
    text1 = data["text1"]
    text2 = data["text2"]
    try:
        result = daplagarism(text1, text2)
        if result[1] == True:
            result[1] = "This is Plagarized by: "
        else:
            result[1] = "This isn't Plagarized. Your plagarism score is: "
    except:
        return "short"
    return f"{result[0]}•{result[1]}•{result[2]}"
