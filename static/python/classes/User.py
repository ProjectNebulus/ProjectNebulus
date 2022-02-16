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
        - username: str - The username of the user.
        - password: str - The password of the user.
        - email: str - The email of the user.
        - created_at: datetime - The date of creation of the user.
    :optional params:
        - courses: List[Course | int] - The courses of the user - Default: []
        - avatar: Avatar - The avatar of the user - Default: None
        - is_staff: bool - Whether the user is a staff member - Default: False
        - student: bool - Whether the user is a student - Default: True
        - teacher: bool - Whether the user is a teacher - Default: False
        - points: int - The amount of Nebulus points the user has - Default: 0
        - bio: str - The bio of the user - Default: None
        - premium: bool - Whether the user has a premium subscription - Default: False
        - premium_expiration: datetime - The date of expiration of the premium subscription - Default: None
        - status: str - The status of the user - Default: None
        - schoology: Schoology - The user's schoology account information - Default: None
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
    points: Optional[int] = 0
    premium: bool = False
    is_staff: bool = False
    student: bool = True
    teacher: bool = False

