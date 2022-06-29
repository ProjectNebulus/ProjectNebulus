import graphene

from . import graphene_models as gm
from .graphql_mutations.core import DBMutations
from .graphql_query import Query

schema = graphene.Schema(
    query=Query,
    mutation=DBMutations,
    types=[
        gm.User,
        gm.Course,
        gm.Folder,
        gm.DocumentFile,
        gm.Event,
        gm.Assignment,
        gm.Grades,
        gm.Avatar,
        gm.Schoology,
        gm.Announcement,
    ],
)
