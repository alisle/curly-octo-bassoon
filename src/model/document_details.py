from dataclasses import dataclass
from dataclasses_json import dataclass_json

from typing import List
from enum import Enum


from .human import Human


class DocumentType:
    GDRIVE : str = "GDrive"

    def __str__(self) -> str:
        return self.name



@dataclass_json
@dataclass(frozen=True, eq=True)
class DocumentDetails:
    document_type : DocumentType
    document_name : str
    document_owners : List[Human]
    document_id : str
    shared : bool
    shared_user : Human
    last_modifed : str
    
        
    