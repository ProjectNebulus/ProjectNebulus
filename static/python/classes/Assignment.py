from collections import dataclass
from typing import List
from datetime import datetime

@dataclass
class Assignment:
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
    due: datetime.date
    description: str = None
    title: str
    _id: int
    points: int = 100



