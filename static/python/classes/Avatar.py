from dataclasses import dataclass

from .AvatarSize import AvatarSize


@dataclass
class Avatar:
    avatar_url: str
    avatar_size: AvatarSize
