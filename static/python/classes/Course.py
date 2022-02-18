from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
# Relative imports (because this directory is a module
from .Folder import Folder
from .Assignment import Assignment
from .Grades import Grades
from .Snowflake import Snowflake
from .Events import Event

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
    created_at: datetime
    template: Optional[str] = None
    teacher: Optional[str] = None
    authorizedUserIds: List[int] = field(default_factory=list)
    assignments: List[Assignment] = field(default_factory=list)
    teacherAccountId: Optional[int] = None
    folders: List[Folder] = field(default_factory=list)
    imported_from: Optional[str] = None
    description: Optional[str] = None
    grades: Optional[Grades] = None
    events: List[Event] = field(default_factory=list)
    updates: list = field(default_factory=list)
