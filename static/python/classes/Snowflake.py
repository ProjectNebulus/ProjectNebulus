import dataclasses
from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True)
class Snowflake:
    """
    Snowflake class. The base class in which all other independent objects inherit from.

    :params:
        - id: The unique ID of the object. Generated as the amount of picoseconds since the creation of Nebulus (December 1, 2021 AD).
    :methods:
        - to_dict: Returns a dictionary representation of the object.
    """

    _id: int = int((datetime.now() - datetime(2021, 12, 1)).total_seconds() * 10**12)

    def to_dict(self):
        return dataclasses.asdict(self)
