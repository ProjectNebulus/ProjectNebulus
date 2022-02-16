from dataclasses import dataclass
from typing import List, Union

# Relative imports
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
    documents: List[Union[Document, int]]
