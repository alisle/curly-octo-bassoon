import abc
from pprint import pprint
from typing import (Any, TypeVar, List)
from dataclasses import (MISSING,
                         _is_dataclass_instance,
                         fields,
                         dataclass
                         )
import logging
from .vertex import _GremlinVertex
from .edge import _GremlinEdge

class GremlinVertexMixin(abc.ABC):    
    def gremlin_get_primary_key(self):
        return self.__class__._gremlin_config.primary_key
    def gremlin_get_label(self):
        return self.__class__._gremlin_config.label
    def gremlin_get_primary_key_value(self):
        if self.__class__._gremlin_config.primary_key is not None:
            return getattr(self, self.__class__._gremlin_config.primary_key)
        else:
            return None
    
    
    
    def gremlin_get_vertex(self):
        if not hasattr(self, "_gremlin_cached"):
            setattr(self, "_gremlin_cached", self.gremlin_create_vertex())
        
        return self._gremlin_cached

    def gremlin_create_vertex(self):
        
        if _is_dataclass_instance(self):
            properties = {}
            edges = []
            for field in fields(self):                
                name = field.name
                value = getattr(self, field.name)
                if isinstance(value, str):
                    logging.info(f"found string: {name}:{value}")
                    properties[name] = value
                elif isinstance(value, (int, float, complex)):
                    logging.info(f"found number: {name}:{str(value)}")
                    properties[name] = value
                elif issubclass(type(value), GremlinVertexMixin):
                    logging.info(f"found edge with no properties: {name}")
                    edges.append((name, value.gremlin_get_node()))                    
                else:
                    logging.warn(f"unknown instance {name}:{value}")                
        else:
            raise RuntimeError("Only able to process dataclasses")

        node = _GremlinVertex(self.gremlin_get_label(),
            self.gremlin_get_primary_key(),
            self.gremlin_get_primary_key_value(),
            properties,
            edges
        )

        return node



def gremlin_vertex(_cls=None, *, primary_key = None):
    def _process_gremlin_vertex(cls, label: str, primary_key: str):
        cls._gremlin_config = _GremlinVertexConfig(primary_key=primary_key, label=label)
        cls._gremlin_config.primary_key = primary_key
        cls._gremlin_config.label = label

        cls.gremlin_get_primary_key = GremlinVertexMixin.gremlin_get_primary_key
        cls.gremlin_get_label = GremlinVertexMixin.gremlin_get_label
        cls.gremlin_get_primary_key_value = GremlinVertexMixin.gremlin_get_primary_key_value        
        cls.gremlin_get_vertex = GremlinVertexMixin.gremlin_get_vertex
        cls.gremlin_create_vertex = GremlinVertexMixin.gremlin_create_vertex

        GremlinVertexMixin.register(cls)

        return cls

    def wrap(cls):
        _process_gremlin_vertex(cls, label=cls.__name__, primary_key=primary_key)
        return cls 
        

    if _cls is None:
        return wrap

    return wrap(_cls)


@dataclass
class _GremlinVertexConfig:
    primary_key : str
    label : str
