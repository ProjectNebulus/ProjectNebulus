from functools import wraps
from flask import request, render_template
from ipaddress import ip_network


def private_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        a = ip_network(
            user_ip, strict=False
        ).network_address
        # the first parameter should be the flask server ip address, so change it to what the ip is for your server
        b = ip_network("127.0.0.1", strict=False).network_address # localhost

        print(b)
        if a == b:
            return func(*args, **kwargs)
        else:
            return render_template("errors/404.html", error="Unauthorized Access")

    return wrapper