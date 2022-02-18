from dataclasses import dataclass, field
from typing import List
from .Document import Document
from .Snowflake import Snowflake


@dataclass
class Folder(Snowflake):
    """
    A class that represents a Folder of Documents
    :params:
        name: The name of the folder
        documents: A list of Document objects inside the folder
    """
    name: str
    documents: List[Document] = field(default_factory=list)