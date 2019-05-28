"""
This file defines the basic functions for clique graphs.
"""
import networkx as nx
import itertools as itert
import math


def clique_graph(g, cmax=math.inf):
    """The clique graph function

    Args:
      g (networkx.classes.graph.Graph): graph
      cmax ([int]): upper bound accepted for order of clique graph

    Returns:
      networkx.classes.graph.Graph: the clique graph of g

    Example:
      >>> from pycliques.cliques import clique_graph
      >>> import networkx as nx
      >>> g=clique_graph(nx.octahedral_graph())
      >>> g.nodes()
      NodeView((frozenset({0, 1, 2}), frozenset({0, 1, 3}), frozenset({0, 2, 4}), frozenset({0, 3, 4}), frozenset({1, 2, 5}), frozenset({1, 3, 5}), frozenset({2, 4, 5}), frozenset({3, 4, 5})))

    """
    ite = nx.find_cliques(g)
    cliques = []
    K = nx.Graph()
    while True:
        try:
            cli = next(ite)
            cliques.append(frozenset(cli))
            if len(cliques) > cmax:
                return None
        except StopIteration:
            break
    K.add_nodes_from(cliques)
    clique_pairs = itert.combinations(cliques, 2)
    K.add_edges_from((c1, c2) for (c1, c2) in clique_pairs if c1 & c2)
    return K


