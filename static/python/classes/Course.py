from collections import dataclass
from teacher import Teacher
from typing import List
from Assignment import Assignment


@dataclass
class Course:
    """
    A class for representing a course.
    """
    name: str
    _id: str
    teacher: str
    assignments: List[Assignment] = []
    teacherAccount: User = None
