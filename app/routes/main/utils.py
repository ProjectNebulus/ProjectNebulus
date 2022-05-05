import datetime
from functools import wraps
from ...static.python.mongodb import read
from flask import session, redirect, request, render_template


def logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username"):
            return func(*args, **kwargs)

        else:
            try:
                read.find_user(username=session.get("username"))
                return redirect("/signin")
            except:
                return redirect("/logout")


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

        if str(user_ip) == "127.0.0.1" or "2600:1700:5450:7b08:9806:a9a9:a039:e92e": #server ip
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
