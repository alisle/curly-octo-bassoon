from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

class APIType(str, Enum):
    HUBSPOT : str = "HUBSPOT"
    GOOGLE : str = "Google" 

@dataclass_json
@dataclass
class APIDetails:
    api_type : APIType
