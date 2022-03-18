# Imports

from flask import Flask, Blueprint, render_template, session, redirect
import os
from flask_mail import Mail, Message
from graphql_server.flask import GraphQLView
from app.static.python.classes.GraphQL.graphql_schema import schema
from functools import wraps

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
    mail = Mail(app)

    with app.app_context():
        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view(
                "graphql", schema=schema.graphql_schema, graphiql=True
            ),
        )

        # Import parts of the application
        def logged_in(f):
            @wraps(f)
            def wrap(*args, **kwargs):
                if not session.get("logged_in"):
                    session.clear()
                    return redirect("/signin")
                return f(*args, **kwargs)

            return wrap

        # Register blueprints

        @simple_page.errorhandler(404)
        @simple_page.errorhandler(405)
        def error_404(e):
            return render_template("errors/404.html")

        @simple_page.errorhandler(500)
        def error_500(e):
            return render_template("errors/500.html")

    return app
