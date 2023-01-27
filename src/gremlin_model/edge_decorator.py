import abc
from pprint import pprint
from typing import (Any, TypeVar, List)
from dataclasses import (MISSING,
                         _is_dataclass_instance,
                         fields,
                         dataclass
                         )
import logging
from .edge import _GremlinEdge
from .vertex_decorator import GremlinVertexMixin

class GremlinEdgeMixin(abc.ABC):    
    def gremlin_get_label(self):
        return self.__class__._gremlin_config.label

    def gremlin_get_source_name(self):
        return self.__class__._gremlin_config.source
    
    def gremlin_get_sink_name(self):
        return self.__class__._gremlin_config.sink

    def gremlin_get_source(self):
        if self.gremlin_get_source_name() is not None:
            vertex = getattr(self, self.gremlin_get_source_name())
            if issubclass(type(vertex), GremlinVertexMixin):
                return vertex

        raise RuntimeError("Only able to process dataclasses") 
        
    def gremlin_get_sink(self):
        if self.gremlin_get_sink_name() is not None:
            vertex = getattr(self, self.gremlin_get_sink_name())
            if issubclass(type(vertex), GremlinVertexMixin):
                return vertex
                
        raise RuntimeError("Only able to process dataclasses") 
            
    
    
    def gremlin_get_edge(self):
        if not hasattr(self, "_gremlin_cached"):
            self._gremlin_cached = self.gremlin_create_edge()
        
        return self._gremlin_cached

    def gremlin_create_edge(self):
        logging.debug(f"creating edge {self.gremlin_get_source_name()} -> {self.gremlin_get_sink_name()}")

        source = self.gremlin_get_source().gremlin_get_vertex()
        sink = self.gremlin_get_sink().gremlin_get_vertex()

        if _is_dataclass_instance(self):
            properties = {}
            for field in fields(self):                
                name = field.name
                value = getattr(self, field.name)
                                
                if name == self.gremlin_get_sink_name() or name == self.gremlin_get_source_name():
                    continue
                elif isinstance(value, str):
                    logging.info(f"found string: {name}:{value}")
                    properties[name] = value
                elif isinstance(value, (int, float, complex)):
                    logging.info(f"found number: {name}:{str(value)}")
                    properties[name] = value                    
                else:
                    logging.warn(f"unknown instance {name}:{value}")                
        else:
            raise RuntimeError("Only able to process dataclasses")

        edge = _GremlinEdge(label=self.gremlin_get_label(), source=source, sink=sink, propertes=properties)

        return edge



def gremlin_edge(_cls=None, *, source, sink ):
    def _process_gremlin_edge(cls, label: str, source: str, sink: str):
        cls._gremlin_config = _GremlinEdgeConfig(label, source, sink)
        cls.gremlin_get_label = GremlinEdgeMixin.gremlin_get_label
        cls.gremlin_get_source = GremlinEdgeMixin.gremlin_get_source
        cls.gremlin_get_sink = GremlinEdgeMixin.gremlin_get_sink
        cls.gremlin_get_edge = GremlinEdgeMixin.gremlin_get_edge
        cls.gremlin_get_sink_name = GremlinEdgeMixin.gremlin_get_sink_name
        cls.gremlin_get_source_name = GremlinEdgeMixin.gremlin_get_source_name
        cls.gremlin_create_edge = GremlinEdgeMixin.gremlin_create_edge

        GremlinEdgeMixin.register(cls)
        return cls

    def wrap(cls):
        _process_gremlin_edge(cls, label=cls.__name__, source=source, sink=sink)
        return cls 
        

    if _cls is None:
        return wrap

    return wrap(_cls)


@dataclass
class _GremlinEdgeConfig:
    label : str
    source : str
    sink : str
