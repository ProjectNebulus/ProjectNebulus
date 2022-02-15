from dataclasses import dataclass, field
from typing import List, Union

from .Assignment import Assignment
from .Folder import Folder
from .Grades import Grades
from .Snowflake import Snowflake


@dataclass
class Course(Snowflake):
    """
    A class for representing a course.
     :required params:
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
    assignments: List[Union[Assignment, int]] = field(default_factory=list)
    teacherAccountID: int = None
    folders: List[Union[Folder, int]] = field(default_factory=list)
    imported_from: str = None
    description: str = None
    grades: Union[Grades, int] = None
