
"""
This file defines some graphs.
"""

import networkx as nx
from networkx.algorithms.operators.binary import disjoint_union
from networkx.algorithms.operators.unary import complement


def graph_join(g, h):
    join = disjoint_union(g, h)
    ne = [(v, w) for v in range(len(g)) for w in range(len(g), len(g)+len(h))]
    join.add_edges_from(ne)
    return join


def graph_suspension(g):
    return graph_join(nx.empty_graph(2), g)


def suspension_of_cycle(n):
    return graph_suspension(nx.cycle_graph(n))


def complement_of_cycle(n):
    return complement(nx.cycle_graph(n))


def octahedron(n):
    edges = []
    aux_graph = nx.Graph()
    for i in range(n):
        edges.append((2*i, 2*i+1))
    aux_graph.add_edges_from(edges)
    return complement(aux_graph)


snub_dysphenoid = nx.from_graph6_bytes(bytes("GQyuzw", 'utf8'))
