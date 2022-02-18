from datetime import datetime
from dataclasses import dataclass, field
import dataclasses

@dataclass(kw_only=True)
class Snowflake:
    _id: int = int((datetime.now() - datetime(2021, 12, 1)).total_seconds() * 10**12)

    def to_dict(self):
        return dataclasses.asdict(self)
