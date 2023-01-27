from dataclasses import dataclass
from dataclasses_json import dataclass_json

from enum import Enum
from typing import List

from .api_details import APIDetails
from .document_details import DocumentDetails
from .human import Human
from gremlin_model import gremlin_vertex, gremlin_edge



class EntityType(str, Enum):
    DUMMY : str = "dummy"    
    DOCUMENT : str = "document"
    API_HUMAN : str = "api_human"
    API_COMPANY : str = "api_company"
    API_COMPANY_HUMAN : str = "api_company_human"

class EntityMeta(type):
    """A person metaclass"""
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return hasattr(subclass, 'entity_type')

class Entity(metaclass=EntityMeta):
    entity_type : EntityType = EntityType.DUMMY 

@dataclass_json
@dataclass
class Document(metaclass=EntityMeta):
    document_details : DocumentDetails
    possible_company_keywords : List[str]
    possible_human_keywords : List[str]
    entity_type : EntityType = EntityType.DOCUMENT


@dataclass_json
@dataclass
@gremlin_edge(source="human", sink="api_details")
class APIHuman(metaclass=EntityMeta):  
    api_details : APIDetails
    human : Human    
    entity_type : EntityType = EntityType.API_HUMAN



@dataclass
@dataclass_json
class APICompany(metaclass=EntityMeta):
    api_details : APIDetails
    company_name: str
    entity_type: EntityType = EntityType.API_COMPANY

@dataclass
@dataclass_json
class APICompanyHuman(metaclass=EntityMeta):
    api_details: APIDetails
    company_name: str
    human : Human
    entity_type: EntityType = EntityType.API_COMPANY_HUMAN


    


