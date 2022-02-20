from mongoengine import *


class Assignment(Snowflake):
    """
    A Class representing an assignment.
    :required params:
        name: The name of the assignment.
        due: The due date of the assignment. Is a datetime.date object.
        title: The title of the assignment.
        _id: The id of the assignment.
    :optional params:
        description: The description of the assignment. Default: None
        points: The number of points the assignment is worth. Default: 100.
    """
    meta = {'collection': 'Assignments'}
    course = ReferenceField('Course', required=True)
    due = DateTimeField(required=True)
    title = StringField(required=True)
    points = IntField(default=100)
    description = StringField(default='')
    