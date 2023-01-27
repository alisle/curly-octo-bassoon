from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from gremlin_model import gremlin_vertex

class APIType(str, Enum):
    HUBSPOT : str = "HUBSPOT"
    GOOGLE : str = "Google" 

@dataclass_json
@dataclass(eq=True)
@gremlin_vertex(primary_key="api_type")
class APIDetails:
    api_type : APIType
