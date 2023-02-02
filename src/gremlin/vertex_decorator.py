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
from collections.abc import Iterable

def _gremlin_is_simple_value(value) -> bool:
    if isinstance(value, (str, bool, int, float, complex)):
        return True
    
    return False

def _gremlin_parse_field(field, name, edges):
    if isinstance(field, str):
        logging.info(f"found string: {name}:{field}")
        return field
    elif isinstance(field, bool):
        logging.info(f"found bool: {name}:{str(field)}")
        return field
    elif isinstance(field, (int, float, complex)):
        logging.info(f"found number: {name}:{field}")
        return field
    elif issubclass(type(field), GremlinVertexMixin):
        logging.info(f"found edge with no properties: {name}")
        if field is not None:
            edges.append((name, field.gremlin_get_vertex()))                    
    elif isinstance(field, Iterable):
        logging.info(f"found a collection: {name}")
        if field is not None:
            for element in field:
                if _gremlin_is_simple_value(element): 
                    # OK so now we have a simple element, we will need to create a node for each of these elements.
                    logging.warn("skipping element as it's simple.")
                    continue
                elif issubclass(type(element), GremlinVertexMixin):
                    logging.info(f"found edge with no properties")
                    edges.append((name, element.gremlin_get_vertex()))                                        
        else:
            logging.info(f"{name} is None, skipping")
    else:
        logging.warn(f"unknown instance {name}:{field}")  

    return None              


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
                value = _gremlin_parse_field(value, name, edges)
                if value is not None:
                    properties[name] = value
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
