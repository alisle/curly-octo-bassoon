from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __

import logging
import os

from .vertex import _GremlinVertex
from .vertex_decorator import GremlinVertexMixin
from .edge_decorator import GremlinEdgeMixin
from .edge import _GremlinEdge

class GraphDB:
    def __init__(self) -> None:
        if os.getenv('TINKERPOP_SEVER') is not None:
            self.server = os.getenv('TINKERPOP_SEVER')
        else:
            self.server = 'ws://localhost:8182/gremlin'

        logging.debug(f"Setting tinkerpop server to {self.server}")
        self.g = traversal().withRemote(DriverRemoteConnection(self.server,'g'))
    
    def _create_vertex_edge_list(self, vertex : _GremlinVertex, vertexes = None, edges = None):
        if vertex not in vertexes:
            logging.debug(f"adding node {vertex.label} to set")
            vertexes.add(vertex)
        else:
            logging.debug(f"node {vertex.label} is already in set")

        for edge in vertex.edges:
            if edge not in edges:
                logging.debug(f"adding edge {edge.label} to set")
                edges.add(edge)

                if edge.source not in vertexes:
                    logging.debug(f"found source which isn't in set adding {edge.source.label}")
                    self._create_vertex_edge_list(edge.source, vertexes, edges)
                
                if edge.sink not in vertexes:
                    logging.debug(f"found sink which isn't in set adding {edge.sink.label}")
                    self._create_vertex_edge_list(edge.sink, vertexes, edges)


        
    def insert(self, obj):
        if issubclass(type(obj), GremlinVertexMixin):
            self.insert_vertex(obj.gremlin_get_vertex())
        elif issubclass(type(obj), GremlinEdgeMixin):
            self.insert_edge(obj.gremlin_get_edge())
        else:
            raise RuntimeError("Invalid type! Not Vertex or Edge!")

    def insert_edge(self, edge: _GremlinEdge):
        logging.debug(f"inserting edge {edge.label}")

        self.insert_vertex(edge.source)
        self.insert_vertex(edge.sink)

        self._insert_single_edge(edge)

        
    def insert_vertex(self, vertex : _GremlinVertex):
        logging.debug(f"inserting vertex {vertex.label}")

        vertexes = set()
        edges = set()
        self._create_vertex_edge_list(vertex, vertexes, edges)
        for v in vertexes:
            self._insert_single_vertex(v)

        for e in edges:
            self._insert_single_edge(e)
            

    def _insert_single_edge(self, edge: _GremlinEdge):
        e = self.g.V(edge.source.id).as_('source').V(edge.sink.id).coalesce(
            __.inE(edge.label).where(__.outV().as_('source')),
            __.addE(edge.label).from_('source')
        ).next()        

        logging.info(f"Finished adding edge: {e.id}")
        edge.id = e.id

        return e

    def _insert_single_vertex(self, node: _GremlinVertex):        
        logging.info("creating vertex properties")        
        v = __.addV(node.label)
        for key in node.properties:
            logging.info(f"adding property {key}={node.properties[key]}")
            v = v.property(key, node.properties[key])

        logging.info(f"seeing if such a node exists {node.label} PK:{node.primary_key}={node.primary_key_value}")            
        vertex = self.g.V().hasLabel(node.label).has(node.primary_key, node.primary_key_value).fold().coalesce(
            __.unfold(),
            v
        ).next()


        logging.info(f"Finished adding vertex: {vertex.id}")
        node.id = vertex.id

        return vertex
