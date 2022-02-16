from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# local imports
from .Snowflake import Snowflake


@dataclass
class Event(Snowflake):
    title: str
    date: datetime
    description: Optional[str] = None
