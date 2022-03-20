from functools import wraps
from flask import session, redirect


def logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        else:
            return redirect("/signin")

    return wrapper
