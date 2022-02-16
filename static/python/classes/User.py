from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Union, Optional

from .Avatar import Avatar
from .Course import Course
from .Schoology import Schoology
from .Snowflake import Snowflake


@dataclass
class User(Snowflake):
    """
    A class representing a user.
    :required params:
        - username: The username of the user.
        - password: The password of the user.
        - email: The email of the user.
        - created_at: The date of creation of the user. Takes a datetime.DateTime object.
    :optional params:
        - courses: The courses of the user. Default: []
        - avatar: The avatar of the user. Default: None
        - is_staff: Whether the user is a staff member. Default: False
        - student: Whether the user is a student. Default: True
        - teacher: Whether the user is a teacher. Default: False
        - points: The points of the user. Default: 0
        - bio: The bio of the user. Default: None
        - premium: Whether the user has a premium subscription. Default: False
        - premium_expiration: The date of expiration of the premium subscription. Default: None
        - status: The status of the user. Default: None
        - schoology: The user's schoology account information. Default: None
    """

    username: str
    password: str
    email: str
    created_at: datetime
    schoology: Optional[Schoology] = None
    avatar: Optional[Avatar] = None
    bio: Optional[str] = None
    premium_expiration: Optional[datetime] = None
    status: Optional[str] = None
    courses: List[Union[Course, int]] = field(default_factory=list)
    points: int = 0
    premium: bool = False
    is_staff: bool = False
    student: bool = True
    teacher: bool = False

