"""
A *local cutpoint* of a graph :math:`G` is a vertex :math:`x` such that its
open neighborhood :math:`N_{G}(x)` is not connected.
"""

import networkx as nx
from pycliques.surfaces import open_neighborhood


def local_cutpoints(graph):
    """Generator of local cutpoints

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      A generator for the local cutpoints that the graph may have

    Example:
      >>> import networkx as nx
      >>> from pycliques.cutpoints import local_cutpoints
      >>> list(local_cutpoints(nx.path_graph(4)))
      [1, 2]

    """
    for v in graph:
        if not nx.is_connected(open_neighborhood(graph, v)):
            yield v


def has_local_cutpoints(graph):
    """Returns whether a graph has local cutpoints

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      If the graph has local cutpoints, return a list which
      only element is the first cutpoint. Otherwise, return False

    Example:
      >>> from pycliques.cutpoints import has_local_cutpoints
      >>> has_local_cutpoints(nx.path_graph(4))
      [1]
      >>> has_local_cutpoints(nx.complete_graph(4))
      False

    """
    try:
        cutpoints = local_cutpoints(graph)
        return [next(cutpoints)]
    except StopIteration:
        return False
