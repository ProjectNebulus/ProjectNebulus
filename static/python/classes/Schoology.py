from dataclasses import dataclass

@dataclass
class Schoology:
    """
    A class representing a user's Schoology account
    """
    Schoology_request_token: str
    Schoology_request_secret: str
    Schoology_access_token: str
    Schoology_access_secret: str
    school_name: str
    school_url: str
