# Imports
from logging import LogRecord

from flask.logging import logging
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO

socketio = SocketIO()

from .api import *
from .main import *
from .static import *


class _LogFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        message = record.getMessage()
        codes = ("200", "304")

        return all((code not in message for code in codes))


def init_app():
    """
    Creates a flask application.
    """
    from flask import Flask
    import os

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("MONGOPASS")
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config["UPLOAD_FOLDER"] = "/app/static/UserContent/"
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = os.getenv("email")
    app.config["MAIL_PASSWORD"] = os.getenv("password")
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    app.config["SECRET_KEY"] = os.getenv("MONGOPASS")
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api.api_blueprint)
    app.register_blueprint(static_blueprint)

    @app.before_request
    def before_rq():
        # log out users who have deleted accounts
        if "username" in session.keys():
            try:
                read.find_user(username=session.get("username"))
            except KeyError:
                return redirect("/logout")

    mail = Mail(app)
    socketio.init_app(app, logging=False)
    logging.getLogger("werkzeug").addFilter(_LogFilter())
    print(app.url_map)

    return app
