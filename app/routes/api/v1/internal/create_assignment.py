from flask import request
from . import internal
from .....static.python.mongodb.create import createAssignment

@internal.route('/create_assignment', methods=['POST'])
def create_assignment():
    """
    Create an assignment.
    """
    # Get the data from the request.
    data = request.get_json()

    # Create the assignment.
    createAssignment(data)

    # Return the success message.
    return 'success', 200