from flask import session, redirect
from functools import wraps


def logged_in(func):
    @wraps(logged_in)
    def wrapper(*args, **kwargs):
        if 'username' in session and 'password' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/signin')

    return wrapper
