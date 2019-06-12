import networkx as nx
import itertools
from networkx.algorithms.operators.unary import complement


def _adyacency_f(graph, edges):
    vertices = []
    for edge in edges:
        vertices.extend(edge)
    subgraph = graph.subgraph(vertices)
    for vertex in subgraph.nodes():
        if subgraph.degree(vertex) != 1:
            return False
    else:
        return True


def induced_octahedra(graph):
    complement_graph = complement(graph)
    aux_graph = nx.Graph()
    edges_complement = complement_graph.edges()
    aux_graph.add_nodes_from(edges_complement)
    edges_pairs = itertools.combinations(edges_complement, 2)
    aux_graph.add_edges_from((e1, e2) for (e1, e2) in edges_pairs if _adyacency_f(complement_graph, (e1, e2)))
    




