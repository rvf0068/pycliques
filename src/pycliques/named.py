
"""
This file defines some graphs.
"""

import networkx as nx
from networkx.algorithms.operators.binary import disjoint_union


def graph_join(g, h):
    join = disjoint_union(g, h)
    ne = [(v, w) for v in range(len(g)) for w in range(len(g), len(g)+len(h))]
    join.add_edges_from(ne)
    return join


def graph_suspension(g):
    return graph_join(nx.empty_graph(2), g)


def suspension_of_cycle(n):
    return graph_suspension(nx.cycle_graph(n))


octa = nx.octahedral_graph()
path5 = nx.path_graph(5)
cyc3 = nx.cycle_graph(3)
