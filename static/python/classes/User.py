from collections import dataclass
from typing import List
from Course import Course
from Avatar import Avatar
from datetime import datetime

@dataclass
class User:
    _id: int
    username: str
    password: str
    email: str
    courses: List[Course]
    points: int = 0
    avatar: Avatar = None
    bio: str = None
    premium: bool = False
    premium_expiration: datetime.date = None
    status: str = None
    created_at: datetime.DateTime = datetime.now()
    is_staff: bool = False






