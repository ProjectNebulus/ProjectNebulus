# Imports
import os

from flask import Flask
from flask_mail import Mail
from flask_cors import CORS

from .api import *
from .main import *
from .static import *


# import app.routes.error_handlers


def init_app():
    """
    Creates a flask application.
    """
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = os.getenv("email")
    app.config["MAIL_PASSWORD"] = os.getenv("password")
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api.api_blueprint)
    app.register_blueprint(static_blueprint)
    mail = Mail(app)
    print([str(p) for p in app.url_map.iter_rules()])

    return app
