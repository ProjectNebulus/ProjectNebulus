from dataclasses import dataclass
from datetime import datetime
from typing import List

from .Snowflake import Snowflake


@dataclass
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

    due: datetime
    title: str
    points: int = 100
    description: str = None
