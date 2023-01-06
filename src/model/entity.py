from dataclasses import dataclass
from dataclasses_json import dataclass_json

from enum import Enum

from .api_details import APIDetails
from .document_details import DocumentDetails
from .human import Human




class EntityType(str, Enum):
    ID : str = "ID"

@dataclass_json
@dataclass
class DocumentEntity:
    document_details : DocumentDetails
    entity_type : EntityType
    entity_value : str

@dataclass_json
@dataclass
class APIEntity:
    api_details : APIDetails
    entity_type : EntityType
    entity_value : str

@dataclass_json
@dataclass
class APIHumanEntity:
    api_details : APIDetails
    human : Human

    


