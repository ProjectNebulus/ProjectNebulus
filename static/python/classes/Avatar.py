from dataclasses import dataclass
from typing import Optional
from .AvatarSize import AvatarSize


@dataclass
class Avatar:
    """
    Class to represent an avatar.

    :params:
        - url: The url of the avatar image.
        - size: The size of the avatar image. Takes in an AvatarSize Object.
    """

    avatar_url: str
    avatar_size: Optional[AvatarSize] = None
