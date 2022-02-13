from dataclasses import dataclass
from datetime import datetime

@dataclass
class Document:
    """
    Class to represent a document. A document is basically a file.
    :required params:
        - _id: The Document's unique identifier.
        - name: The Document's name.
        - url: The Document's url.
        - upload_date: The Document's creation date.
    :optional params:
        - description: The Document's description.
    """
    _id: int
    url: str
    name: str
    upload_date: datetime.DateTime
    description: str = None