from dataclasses import dataclass, field
from typing import List

from Assignment import Assignment
from Folder import Folder
from Grades import Grades
from Snowflake import Snowflake
from User import User


@dataclass
class Course(Snowflake):
    """
    A class for representing a course.
     :required params:
        - _id: The id of the course.
        - name: The name of the course.
        - teacher: The teacher of the course.
    :optional params:
        - assignments: A list of Assignment Objects for the course. Default: []
        - teacherAccount: The account of the teacher. Default: None (Because some teachers may not have an account)
        - imported_from: The LMS this course was imported from. Default: None
        - folders: A list of Folder Objects for the course. Default: []
        - description: The course description. Default: None
        - grades: A Grades Object for the course. Represents the user's grades. Default: None

    """

    name: str
    teacher: str
    assignments: List[Assignment] = field(default_factory=list)
    teacherAccount: User = None
    folders: List[Folder] = field(default_factory=list)
    imported_from: str = None
    description: str = None
    grades: Grades = None
