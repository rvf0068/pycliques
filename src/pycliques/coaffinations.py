"""
A *coaffination* of a graph :math:`G` is an automorphism
:math:`\sigma\colon G\\to G` such that the distance from
:math:`\sigma(x)` to :math:`x` is at least 2 for each vertex
:math:`x`.
"""

import networkx as nx
from networkx.algorithms import isomorphism
from pycliques.utilities import invert_dict
from grandiso import find_motifs_iter


class CoaffinePair(object):
    def __init__(self, graph, coaffination):
        self.graph = graph
        self.coaffination = coaffination


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


def has_coaffinations(graph, k):
    """Returns whether a graph has coaffinations

    Args:
      graph (networkx.classes.graph.Graph): graph
      k ([int]): distance required between each vertex and its image

    Returns:
      If the graph has coaffinations, return a list which
      only element is the first coaffination. Otherwise, return False

    Example:
      >>> from pycliques.coaffinations import has_coaffinations
      >>> has_coaffinations(nx.path_graph(4), 2)
      False
      >>> has_coaffinations(nx.octahedral_graph(), 2)
      [{5: 0, 4: 1, 3: 2, 2: 3, 1: 4, 0: 5}]

    """
    try:
        coaffs = coaffinations(graph, k)
        return [next(coaffs)]
    except StopIteration:
        return False


def is_coaffine_map(pair1, pair2, dmap):
    sigma1 = pair1.coaffination
    sigma2 = pair2.coaffination
    for x in pair1.graph:
        if dmap[sigma1[x]] != sigma2[dmap[x]]:
            return x
    return True


def coaffine_monomorphism(large_pair, small_pair, algorithm="GM"):
    """Find a coaffine monomorphism from `large_pair` to `small_pair`"""
    g1 = small_pair.graph
    g2 = large_pair.graph
    if algorithm == "GM":
        GM = nx.isomorphism.GraphMatcher(g2, g1)
        the_iter = GM.subgraph_monomorphisms_iter()
    elif algorithm == "Grandiso":
        the_iter = find_motifs_iter(g1, g2)
    for mono in the_iter:
        if algorithm == "GM":
            mono = invert_dict(mono)
        if is_coaffine_map(small_pair, large_pair, mono) is True:
            return mono
    return False
