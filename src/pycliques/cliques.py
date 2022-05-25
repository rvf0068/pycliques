"""
This file defines a function for the clique graph. It is basically
the same as ``networkx.algorithms.clique.make_max_clique_graph``, but
includes a parameter to abort the construction in case the graph has
too many vertices.
"""

import networkx as nx
import numpy as np
import itertools
import math


class Clique(frozenset):
    def __repr__(self):
        u = set(self)
        if len(u) == 0:
            return "{}"
        else:
            return f"{u}"


def clique_graph(graph, bound=math.inf):
    """The clique graph function

    Args:
      graph (networkx.classes.graph.Graph): graph
      bound ([int]): upper bound accepted for order of clique graph

    Returns:
      networkx.classes.graph.Graph: the clique graph of g

    Return type:
      NetworkX graph

    Example:
      >>> import networkx as nx
      >>> from pycliques.cliques import clique_graph
      >>> g=clique_graph(nx.octahedral_graph())
      >>> g.nodes()
      NodeView(({0, 1, 2}, {0, 1, 3}, {0, 2, 4}, {0, 3, 4}, {1, 2, 5}, {1, 3, 5}, {2, 4, 5}, {3, 4, 5}))

    """
    it_cliques = nx.find_cliques(graph)
    cliques = []
    K = nx.Graph()
    while True:
        try:
            clique = next(it_cliques)
            cliques.append(Clique(clique))
            if len(cliques) > bound:
                return None
        except StopIteration:
            break
    K.add_nodes_from(cliques)
    clique_pairs = itertools.combinations(cliques, 2)
    K.add_edges_from((c1, c2) for (c1, c2) in clique_pairs if c1 & c2)
    return K


def pos_clique(graph, pos, bound=math.inf):
    K = clique_graph(graph, bound)
    posK = dict()
    if K:
        for clique in K:
            posK[clique] = np.mean([pos[x] for x in clique], axis=0)
        return posK
