from dataclasses import dataclass, field
from typing import List
from Course import Course
from Avatar import Avatar
from datetime import datetime
from Schoology import Schoology

@dataclass
class User:
    """
    A class representing a user.
    :required params:
        - _id: The id of the user.
        - username: The username of the user.
        - password: The password of the user.
        - email: The email of the user.
    :optional params:
        - courses: The courses of the user. Default: []
        - avatar: The avatar of the user. Default: None
        - created_at: The date of creation of the user. Default: datetime.now()
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
    _id: int
    username: str
    password: str
    email: str
    courses: List[Course] = field(default_factory=list)
    points: int = 0
    avatar: Avatar = None
    bio: str = None
    premium: bool = False
    premium_expiration: datetime.date = None
    status: str = None
    created_at: datetime.DateTime = datetime.now()
    is_staff: bool = False
    student: bool = True
    teacher: bool = False
    schoology: Schoology = None






