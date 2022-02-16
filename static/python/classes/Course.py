from dataclasses import dataclass, field
from typing import (
    List,
    Optional,
    Union
)

# Local imports
from .Assignment import Assignment
from .Folder import Folder
from .Grades import Grades
from .Snowflake import Snowflake
from .Avatar import Avatar
from .Events import Event


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
        - authorizedUserIds: A list of user IDs that are authorized to view the course. Default: []

    """

    name: str
    teacher: str
    imported_from: Optional[str] = None
    description: Optional[str] = None
    grades: Optional[Union[Grades, int]] = None
    teacherAccountID: Optional[int] = None
    assignments: List[Union[Assignment, int]] = field(default_factory=list)
    folders: List[Union[Folder, int]] = field(default_factory=list)
    image: Optional[Avatar] = None
    events: List[Union[Event, int]] = field(default_factory=list)
    authorizedUserIDs: List[int] = field(default_factory=list)
