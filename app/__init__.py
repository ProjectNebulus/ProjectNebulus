# todo: import "schema"

from flask import Flask
from graphql_server.flask import GraphQLView


def init_app():
    """
    Creates a flask application.
    """
    app = Flask(__name__)

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

        return app
