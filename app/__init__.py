from flask import Flask


def init_app():
    """
    Creates a flask application.
    """
    app = Flask(__name__)

    # todo: blueprints
    with app.app_context():
        # Import parts of the application

        # Register blueprints

        return app
