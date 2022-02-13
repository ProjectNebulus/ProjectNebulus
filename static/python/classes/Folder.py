from dataclasses import dataclass
from typing import List
from Document import Document

@dataclass
class Folder:
    """
    A class that represents a Folder of Documents
    :params:
        name: The name of the folder
        documents: A list of Document objects inside the folder
        _id: The id of the folder
    """
    name: str
    documents: List[Document]
    _id: str