# Imports
from logging import LogRecord
import eventlet

eventlet.monkey_patch()
from flask import has_request_context
from flask.logging import logging, default_handler
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO

socketio = SocketIO()
mail = Mail()
from .api import *
from .main import *
from .static import *


class _LogFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        message = record.getMessage()
        keywords = ("200", "304")

        return all((word not in message for word in keywords))


class _LogFormatter(logging.Formatter):
    prevMessage = ""
    occurrences = 1

    def format(self, record: LogRecord) -> str:
        occurring = (message := record.getMessage()) == self.prevMessage
        if occurring:
            self.occurrences += 1
        else:
            self.prevMessage = message
            self.occurrences = 1

        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        if occurring:
            return f"\n[{self.occurrences}x occurred]"
        else:
            return super().format(record)


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
        if "id" in session.keys():
            try:
                read.find_user(id=session.get("id"))
            except KeyError:
                return redirect("/logout")

    mail.init_app(app)
    logging.getLogger("werkzeug").addFilter(_LogFilter())
    default_handler.setFormatter(_LogFormatter())
    socketio.init_app(app, async_mode="eventlet")

    return app
