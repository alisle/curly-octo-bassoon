from dataclasses import dataclass
from dataclasses_json import dataclass_json
from gremlin import gremlin_vertex

@dataclass(eq=True)
@dataclass_json
@gremlin_vertex(primary_key="company_name")
class Company:
    display_name: str
