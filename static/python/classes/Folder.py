from dataclasses import dataclass
from typing import List
from Document import Document

@dataclass
class Folder:
    """
    A class that represents a Folder of Documents
    """
    name: str
    documents: List[Document]
    _id: str