from flask_graphql import GraphQLView

from . import api_blueprint
from ...static.python.classes.GraphQL.graphql_schema import schema

api_blueprint.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema.graphql_schema, graphiql=True
    ),
)
