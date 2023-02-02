

class _GremlinEdge:
    id : int = None
    label = None
    source = None
    sink = None
    propertes = None

    def __init__(self, label, source, sink, propertes = None) -> None:
        self.label = label
        self.source = source
        self.sink = sink
        self.propertes = propertes
        
    def __eq__(self, other):
        return other and self.label == other.label and self.source == other.source and self.sink == other.sink

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.label, self.source, self.sink))