"""
A *coaffination* of a graph :math:`G` is an automorphism
:math:`\sigma\colon G\\to G` such that the distance from
:math:`\sigma(x)` to :math:`x` is at least 2 for each vertex
:math:`x`.
"""

import networkx as nx
from networkx.algorithms import isomorphism


def automorphisms(graph):
    """Generator of automorphisms

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      A generator for the automorphisms that the graph may have

    Example:
      >>> import networkx as nx
      >>> from pycliques.coaffinations import automorphisms
      >>> list(automorphisms(nx.cycle_graph(3)))
      [{0: 0, 1: 1, 2: 2}, {0: 0, 2: 1, 1: 2}, {1: 0, 0: 1, 2: 2}, {1: 0, 2: 1, 0: 2}, {2: 0, 0: 1, 1: 2}, {2: 0, 1: 1, 0: 2}]

    """
    GM = isomorphism.GraphMatcher(graph, graph)
    return GM.subgraph_isomorphisms_iter()


def coaffinations(graph, k):
    """Generator of coaffinations

    Args:
      graph (networkx.classes.graph.Graph): graph
      k ([int]): distance required between each vertex and its image

    Returns:
      A generator for the coaffinations that the graph may have

    Example:
      >>> import networkx as nx
      >>> from pycliques.coaffinations import coaffinations
      >>> list(coaffinations(nx.octahedral_graph(),2))
      [{5: 0, 4: 1, 3: 2, 2: 3, 1: 4, 0: 5}]

    """
    the_automorphisms = automorphisms(graph)
    distance = dict(nx.all_pairs_shortest_path_length(graph))
    for auto in the_automorphisms:
        for v in graph:
            if distance[v][auto[v]] < k:
                break
        else:
            yield auto
