# Imports
from flask_cors import CORS
from flask_mail import Mail

from .api import *
from .main import *
from .static import *


# import app.routes.error_handlers


def init_app():
    """
    Creates a flask application.
    """
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
            #log out users who have deleted accounts
            if "username" in session.keys():
                try:
                    read.find_user(username=session.get("username"))
                except:
                    return redirect("/logout")

    mail = Mail(app)
    #print("Paths:", *sorted(app.url_map.iter_rules(), key=str), sep="\n")

    return app
