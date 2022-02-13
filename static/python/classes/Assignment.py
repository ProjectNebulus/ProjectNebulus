from collections import dataclass
from typing import List
from datetime import datetime
@dataclass
class Assignment:
    due: datetime.date
    description: str = ""
    title: str
    _id: int



