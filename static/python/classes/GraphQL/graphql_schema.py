import graphene
from .graphql_query import Query
from .graphql_mutations.core import DBMutations
from . import graphene_models as gm


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
        gm.AvatarSize,
        gm.Schoology,
        gm.Announcement,
    ],
)