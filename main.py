"""
App entrypoint.
"""
from app.routes import init_app
from waitress import serve

import flask, re, os
from app.static.python.mongodb import read


app = init_app()
print(app.url_map)
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@app.route("/api/v1/internal/check-signin", methods=["POST"])
def signin_username1():
    json = flask.request.get_json()
    validation = read.check_password_username(
        json.get("username"), json.get("password")
    )

    if validation.split("-")[0] == "true" and validation.split("-")[1] == "true":
        if re.fullmatch(regex, json.get("username")):
            # If the username is an email, then we need to get the username from the database
            user = read.find_user(email=json.get("username"))

        else:
            # If the username is not an email, then we need to get the email from the database
            user = read.find_user(username=json.get("username"))

        flask.session["username"] = user.username
        flask.session["email"] = user.email
        flask.session["password"] = json.get("password")
        flask.session["id"] = user.id

    return validation


@app.route("/api/v1/internal/sign-in", methods=["POST"])
def signin_post():
    if not flask.session.get("username") and not flask.session.get("password"):
        return "false"
    flask.session["logged_in"] = True
    return "true"


# app.register_blueprint(error_blueprint)
if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    serve(app=app, host="0.0.0.0", port=8080)
