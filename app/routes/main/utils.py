import datetime
from functools import wraps

from flask import session, redirect, request, render_template


def logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username"):
            return func(*args, **kwargs)
        else:
            return redirect("/signin")

    return wrapper


def private_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.getlist("X-Forwarded-For"):
            user_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            user_ip = request.remote_addr
            print("computer ip")

        # the first parameter should be the flask server ip address, so change it to what the ip is for your server

        if user_ip == "127.0.0.1":
            return func(*args, **kwargs)
        else:
            return render_template("errors/404.html", error="Unauthorized Access")

    return wrapper


def strftime(time: datetime.date, fmt) -> str:
    try:
        return time.strftime(fmt)

    except ValueError:
        if "-" in fmt:
            fmt = fmt.replace("-", "#")
        else:
            fmt = fmt.replace("#", "-")

        return time.strftime(fmt)
