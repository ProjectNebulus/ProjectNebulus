from flask import request

from . import internal
from .....static.python.mongodb import read


@internal.route('/check-signup-user', methods=['POST'])
def check_signin_user():
    validation = read.check_signup_user(**request.form)
    return validation
