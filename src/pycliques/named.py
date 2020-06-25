
"""
This file defines some graphs.
"""

import networkx as nx
from networkx.algorithms.operators.binary import disjoint_union
from networkx.algorithms.operators.unary import complement


def graph_join(g, h):
    """The join of two graphs

    Args:
      g, h (networkx.classes.graph.Graph): graph

    Returns:
      A graph, obtained from the disjoint union of g and h, adding all
      edges joining a vertex of g from a vertex of h. Since it is based
      on networkx's disjoint union, it returns a graph where the node labels
      are integers.

    Example:
      >>> import networkx as nx
      >>> from pycliques.named import graph_join
      >>> graph_join(nx.empty_graph(2), nx.empty_graph(2)).edges()
      EdgeView([(0, 2), (0, 3), (1, 2), (1, 3)])

    """
    join = disjoint_union(g, h)
    ne = [(v, w) for v in range(len(g)) for w in range(len(g), len(g)+len(h))]
    join.add_edges_from(ne)
    return join


def graph_suspension(graph):
    """The suspension of a graph.

    Args:
      g (networkx.classes.graph.Graph): graph

    Returns:
      The suspension of the graph, that is, the graph obtained from graph by
      adjoining two new vertices, (labeled 0 and 1),
      that are made adjacent to all vertices of graph.

    Example:
      >>> import networkx as nx
      >>> from pycliques.named import graph_suspension
      >>> graph_suspension(nx.empty_graph(3)).edges()
      EdgeView([(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)])

    """
    return graph_join(nx.empty_graph(2), graph)


def suspension_of_cycle(n):
    """The suspension of the cycle graph of order n.

    Args:
      n (int): integer

    Returns:
      graph: A NetworkX graph.

    Examples:
      >>> import networkx as nx
      >>> from pycliques.named import suspension_of_cycle
      >>> nx.is_isomorphic(nx.octahedral_graph(), suspension_of_cycle(4))
      True

    """
    return graph_suspension(nx.cycle_graph(n))


def complement_of_cycle(n):
    """The complement of the cycle graph of order n.

    Args:
      n (int): integer

    Returns:
      graph: A NetworkX graph.

    Examples:
      >>> from pycliques.named import complement_of_cycle
      >>> from pycliques.helly import is_clique_helly
      >>> is_clique_helly(complement_of_cycle(6))
      True
      >>> is_clique_helly(complement_of_cycle(7))
      True
      >>> is_clique_helly(complement_of_cycle(8))
      False

    """
    return complement(nx.cycle_graph(n))


def octahedron(n):
    """The n-th octahedron.

    Args:
      n (int): integer

    Returns:
      graph: A NetworkX graph. The complement of n disjoint edges.

    Examples:
      >>> from pycliques.named import octahedron
      >>> nx.is_isomorphic(nx.octahedral_graph(), octahedron(3))
      True
      >>> nx.complement(octahedron(4)).edges()
      EdgeView([(0, 1), (2, 3), (4, 5), (6, 7)])

    """
    edges = []
    aux_graph = nx.Graph()
    for i in range(n):
        edges.append((2*i, 2*i+1))
    aux_graph.add_edges_from(edges)
    return complement(aux_graph)


def snub_dysphenoid():
    """Returns the snub dysphenoid graph."""
    return nx.from_graph6_bytes(bytes("GQyuzw", 'utf8'))
