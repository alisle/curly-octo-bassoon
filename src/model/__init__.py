from enum import Enum
from typing import List
from pprint import pprint
import json

class ModelMessage: 
    def to_json(self):
        return json.dumps(self, default= lambda o: o.__dict__, sort_keys=True, indent=4)


class DocumentGroupType(str, Enum):
    SENTENCE : str = "Sentence"
    ROW: str = "Row"
    
class DocumentType(str, Enum):
    GDRIVE : str = "GDrive"

    def __str__(self) -> str:
        return self.name

class DocumentUser(ModelMessage):
    def __init__(self, display_name: str, email_address: str) -> None:
        self.display_name = display_name
        self.email_address = email_address

    def _decoder(modelDict : dict): 
        return DocumentUser(modelDict['display_name'], modelDict['email_address'])
    
    def from_json(raw : bytes):
        return json.loads(raw.decode('utf-8'), object_hook=DocumentUser._decoder)
        

class DocumentDetails(ModelMessage):
    def __init__(self, document_type : DocumentType, document_name : str, document_owners: List[DocumentUser], document_id: str, shared: bool, shared_by : DocumentUser , last_modified: str) -> None:
        self.document_type = document_type
        self.document_name = document_name
        self.document_owners = document_owners
        self.document_id = document_id
        self.last_modifed = last_modified
        self.shared = shared
        self.shared_by = shared_by
        
    

class EntityType(str, Enum):
    ID : str = "ID"

class Entity(ModelMessage):
    def __init__(self, document_details: DocumentDetails, entity_type: EntityType, entity_value: str) -> None:
        self.document_details = document_details
        self.entity_type = entity_type
        self.entity_value = entity_value

                

    def __str__(self):
        return f"DT: {self.document_details.document_type}, DID: {self.document_details.document_id}, ET: {self.entity_type}, EV: {self.entity_value}"
            


