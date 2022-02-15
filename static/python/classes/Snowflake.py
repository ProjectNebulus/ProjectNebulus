
from datetime import datetime
from dataclasses import dataclass, field
import dataclasses

@dataclass()
class Snowflake:
    _id: int = field(default=0, init=False)

    def __post_init__(self):
        self._id = ((datetime.now() - datetime(2021, 12, 1)).total_seconds() * 1000)
        self.__dict__['_id'] = self._id

    def to_dict(self, storeById=False):
        if storeById:
            for x, y in self.__dict__.items():
                if isinstance(y, list):
                    if all(dataclasses.is_dataclass(z) for z in y):
                        self.__dict__[x] = [z._id for z in y]

                elif dataclasses.is_dataclass(y):
                    if not hasattr(y, '_id'):
                        self.__dict__[x] = y.__dict__
                    if not hasattr(y, 'to_dict'):
                        self.__dict__[x] = y._id
                    else:
                        self.__dict__[x] = y._id
            return self.__dict__

        for x, y in self.__dict__.items():
            if isinstance(y, list):
                if all(dataclasses.is_dataclass(z) for z in y):
                    self.__dict__[x] = [z.to_dict() for z in y]

            elif dataclasses.is_dataclass(y):
                if not hasattr(y, 'to_dict'):
                    self.__dict__[x] = y.__dict__
                else:
                    self.__dict__[x] = y.to_dict()
        return self.__dict__

