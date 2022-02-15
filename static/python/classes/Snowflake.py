from datetime import datetime
from dataclasses import dataclass
import dataclasses

@dataclass(kw_only=True)
class Snowflake:
    _id: int = int((datetime.now() - datetime(2021, 12, 1)).total_seconds() * 10**13)

    def to_dict(self):
        return dataclasses.asdict(self)

