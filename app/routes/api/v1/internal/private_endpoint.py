from functools import wraps
from flask import request, render_template
from ipaddress import ip_network


def private_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        a = ip_network(
            request.headers["X-Appengine-User-Ip"], strict=False
        ).network_address
        b = ip_network(request.remote_addr, strict=False).network_address
        if a == b:
            return func(*args, **kwargs)
        else:
            return render_template("404.html", error="Unauthorized Access")
