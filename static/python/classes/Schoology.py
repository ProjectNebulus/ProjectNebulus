from dataclasses import dataclass
from typing import Optional


@dataclass
class Schoology:
    """
    A class representing a user's Schoology account
    """

    Schoology_request_token: Optional[str] = None
    Schoology_request_secret: Optional[str] = None
    Schoology_access_token: Optional[str] = None
    Schoology_access_secret: Optional[str] = None
    schoologyName: Optional[str] = None
    schoologyEmail: Optional[str] = None
