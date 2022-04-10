from flask import request
import datetime
from . import internal
from .....static.python.mongodb.create import createAssignment


@internal.route("/create-assignment", methods=["POST"])
def create_assignment():
    """
    Create an assignment.
    """
    # Get the data from the request.
    data = request.get_json()
    data["points"] = int(data["points"])
    date = datetime.datetime.strptime(data["due_date"], "%m/%d/%Y") - datetime.timedelta(days=1)
    del data["due_date"]
    data["due"] = datetime.datetime.combine(date, datetime.time(11, 59, 59))

    # Create the assignment.
    createAssignment(data)

    # Return the success message.
    return "success", 200
