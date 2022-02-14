from dataclasses import dataclass
from datetime import datetime

@dataclass
class Snowflake:
    _id: int = (datetime.now() - datetime(2021, 12, 1)).total_seconds() * 1000