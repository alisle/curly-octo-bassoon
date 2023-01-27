from dataclasses import dataclass
from dataclasses_json import dataclass_json
from gremlin_model import gremlin_vertex

@dataclass_json
@dataclass(eq=True)
@gremlin_vertex(primary_key="email_address")
class Human:
    display_name : str
    email_address : str

