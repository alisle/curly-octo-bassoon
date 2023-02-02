from .edge import _GremlinEdge

class _GremlinVertex:
    id : int = None
    label : str
    primary_key : str
    primary_key_value : str
    properties : dict
    edges = None

    def __init__(self, label : str, primary_key : str, primary_key_value: str, properties : dict, edges) -> None:
        self.label = label
        self.primary_key = primary_key
        self.primary_key_value = primary_key_value
        self.properties = properties
        self.edges = []

        for (label, sink) in edges:
            self.edges.append(_GremlinEdge(label=label, source=self, sink=sink))

    def __eq__(self, other):
        return other and self.label == other.label and self.primary_key == other.primary_key and self.primary_key_value == other.primary_key

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.label, self.primary_key, self.primary_key_value))

