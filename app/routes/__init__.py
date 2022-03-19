# Imports
from flask import Flask
from flask_mail import Mail
import os
from .error_handlers import error_blueprint
from .main import main_blueprint
from .api import api
from .static import static_blueprint


# import app.routes.error_handlers


def init_app():
    """
    Creates a flask application.
    """
    app = Flask(__name__)
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = os.getenv("email")
    app.config["MAIL_PASSWORD"] = os.getenv("password")
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    print(api.url_prefix)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(error_blueprint)
    app.register_blueprint(api)
    app.register_blueprint(static_blueprint)
    mail = Mail(app)
    print([str(p) for p in app.url_map.iter_rules()])

    return app
