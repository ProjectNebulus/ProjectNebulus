# Imports
import logging
import os

import eventlet
from flask import Flask, has_request_context, redirect, request, session
from flask_babel import Babel
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO

eventlet.monkey_patch()

# Global Variables
socketio = SocketIO()
mail = Mail()
babel = Babel()

from app.static.python.mongodb import read

# Blueprints
from .api import api_blueprint
from .main import main_blueprint
from .static import static_blueprint


class LogFilter(logging.Filter):
    """
    Filter class for logging.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        keywords = ("200", "304")

        return all(word not in message for word in keywords)


class LogFormatter(logging.Formatter):
    """
    Formatter class for logging.
    """
    prev_message = ""
    occurrences = 1

    def format(self, record: logging.LogRecord) -> str:
        occurring = (message := record.getMessage()) == self.prev_message
        if occurring:
            self.occurrences += 1
        else:
            self.prev_message = message
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

    # Flask App
    app = Flask(__name__, template_folder="../templates")
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
    app.register_blueprint(api_blueprint)
    app.register_blueprint(static_blueprint)

    # Before Request
    @app.before_request
    def before_request():
        """
        Log out users who have deleted account
        """
        if "id" in session.keys():
            try:
                read.find_user(id=session.get("id"))
            except KeyError:
                return redirect("/logout")

    mail.init_app(app)
    socketio.init_app(app, async_mode="eventlet", cors_allowed_origins="*")

    return app
