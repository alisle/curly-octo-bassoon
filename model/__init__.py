from enum import Enum
import json

class DocumentGroupType(str, Enum):
    SENTENCE : str = "Sentence"
    ROW: str = "Row"
    
class DocumentType(str, Enum):
    GDRIVE : str = "GDrive"

    def __str__(self) -> str:
        return self.name

    

class EntityType(str, Enum):
    ID : str = "ID"

class Entity:
    def __init__(self, document_type : DocumentType, document_id: str, entity_type: EntityType, entity_value: str) -> None:
        self.document_type = document_type
        self.document_id = document_id
        self.entity_type = entity_type
        self.entity_value = entity_value

                

    def __str__(self):
        return f"DT: {self.document_type}, DID: {self.document_id}, ET: {self.entity_type}, EV: {self.entity_value}"
    
    def to_json(self):
        return json.dumps(self, default= lambda o: o.__dict__, sort_keys=True, indent=4)
        


