from dataclasses import dataclass
from dataclasses_json import dataclass_json
from gremlin import gremlin_vertex
from typing import List
from enum import Enum


from .human import Human


class DocumentType(str, Enum):
    GDRIVE : str = "GDrive"

    def __str__(self) -> str:
        return self.name


@dataclass_json
@dataclass(eq=True)
@gremlin_vertex(primary_key="document_id")
class DocumentDetails:
    document_type : DocumentType
    document_name : str
    document_owners : List[Human]
    document_id : str
    shared : bool
    shared_user : Human
    last_modifed : str
    
        
