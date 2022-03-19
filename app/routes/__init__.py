# Imports

from flask import Flask, Blueprint, render_template, session, redirect
import os
from flask_mail import Mail, Message
from graphql_server.flask import GraphQLView
from app.static.python.classes.GraphQL.graphql_schema import schema
import app.routes.about
import app.routes.home
import app.routes.signin
import app.routes.signup
import app.routes.points
import app.routes.pricing
import app.routes.logout
import app.routes.lms
import app.routes.dashboard
import app.routes.settings
import app.routes.profile
import app.routes.connections
import app.routes.courses
import app.routes.error_handlers


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
    return app
