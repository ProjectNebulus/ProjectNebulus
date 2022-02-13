from dataclasses import dataclass, field
from Folder import Folder
from typing import List
from Assignment import Assignment
from User import User


@dataclass
class Course:
    """
    A class for representing a course.
     :required params:
        - _id: The id of the course.
        - name: The name of the course.
        - teacher: The teacher of the course.
    :optional params:
        - assignments: A list of Assignment Objects for the course. Default: []
        - teacherAccount: The account of the teacher. Default: None (Because some teachers may not have an account)
    """
    name: str
    _id: str
    teacher: str
    assignments: List[Assignment] = field(default_factory=list)
    teacherAccount: User = None
    folders: List[Folder] = field(default_factory=list)
    imported_from: str = None
    description: str = None
