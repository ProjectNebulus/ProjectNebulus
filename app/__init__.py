# todo: import "schema"

from flask import Flask, Blueprint, render_template
from graphql_server.flask import GraphQLView
from .static.python.classes.GraphQL.graphql_schema import schema

simple_page = Blueprint("simple_page", __name__, template_folder="templates")


def init_app():
    """
    Creates a flask application.
    """
    app = Flask(__name__)
    app.register_blueprint(simple_page)

    # todo: blueprints
    with app.app_context():
        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view(
                "graphql", schema=schema.graphql_schema, graphiql=True
            ),
        )

        # Import parts of the application

        # Register blueprints
        @simple_page.route("/", defaults={"page": "index"})
        def index():
            return render_template("main/index.html")

        @simple_page.errorhandler(404)
        def error_404(e):
            return render_template("errors/404.html")

        return app
