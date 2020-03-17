"""A vertex :math:`v` of a graph :math:`G` is *dominated* if there is
another vertex :math:`u\ne v` such that :math:`N_{G}[v]\subseteq
N_{G}[u]`. A graph is called *dismantlable* if by removing dominated
vertices we end up with the one-vertex graph. A vertex is called
*s-dismantlable* if its open neighborhood is dismantlable. An edge is
called *s-dismantlable* if the subgraph induced by the common
neighbors of its ends is dismantlable.

"""
import copy

from pycliques.surfaces import open_neighborhood


def closed_neighborhood(graph, v):
    """The closed neighborhood of a vertex in a graph

    Args:
      graph (networkx.classes.graph.Graph): graph
      v: vertex in a graph

    Returns:
      The neighbors of v in graph, as a set.

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import closed_neighborhood
      >>> closed_neighborhood(nx.path_graph(4), 0)
      {0, 1}

    """
    return set(graph[v]) | {v}


def is_dominated_vertex(graph, v):
    """Returns whether a vertex in a graph is dominated

    Args:
      graph (networkx.classes.graph.Graph): graph
      v: vertex in a graph

    Returns:
      True if the vertex v is dominated in graph, False otherwise.

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import is_dominated_vertex
      >>> is_dominated_vertex(nx.path_graph(4), 0)
      True
      >>> is_dominated_vertex(nx.path_graph(4), 1)
      False

    """
    for u in graph:
        if u != v:
            if closed_neighborhood(graph,
                                   v).issubset(closed_neighborhood(graph, u)):
                return True
    else:
        return False


def has_dominated_vertex(graph):
    """Returns whether a graph has dominated vertices

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      If the graph has dominated vertices, returns a list which only element
      is the first dominated vertex. Otherwise, return False

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import has_dominated_vertex
      >>> has_dominated_vertex(nx.path_graph(4))
      [0]
      >>> has_dominated_vertex(nx.cycle_graph(4))
      False

    """

    for v in graph:
        if is_dominated_vertex(graph, v):
            return [v]
    else:
        return False


def remove_dominated_vertex(graph):
    """If a graph has a dominated vertex, returns a graph without it

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      If the graph has dominated vertices, returns a graph with the dominated
      vertex removed. Otherwise, returns a copy of graph.

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import remove_dominated_vertex
      >>> g1 = remove_dominated_vertex(nx.path_graph(4))
      >>> list(g1.nodes())
      [1, 2, 3]
      >>> g2 = remove_dominated_vertex(nx.cycle_graph(4))
      >>> list(g2.nodes())
      [0, 1, 2, 3]

    """
    g1 = copy.deepcopy(graph)
    x = has_dominated_vertex(graph)
    if not x:
        return g1
    else:
        g1.remove_node(x[0])
        return g1


def completely_pared_graph(graph):
    """Remove successively all dominated vertices from a graph

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      The graph obtained by removing all dominated vertices

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import completely_pared_graph
      >>> cp = completely_pared_graph(nx.path_graph(4))
      >>> list(cp.nodes())
      [3]

    """
    g1 = copy.deepcopy(graph)
    while True:
        n = g1.order()
        g1 = remove_dominated_vertex(g1)
        if n == g1.order():
            return g1


def is_dismantlable(graph):
    """Returns whether the graph is dismantlable

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      True if the graph is dismantlable, False otherwise

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import is_dismantlable
      >>> is_dismantlable(nx.path_graph(4))
      True
      >>> is_dismantlable(nx.cycle_graph(4))
      False

    """
    return completely_pared_graph(graph).order() == 1


def is_s_dismantlable_vertex(graph, v):
    """Returns whether a vertex in a graph is s-dismantlable

    Args:
      graph (networkx.classes.graph.Graph): graph
      v: vertex in a graph

    Returns:
      True if the vertex v is s-dismantlable in graph, False otherwise.

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import is_s_dismantlable_vertex
      >>> from pycliques.dominated import is_dominated_vertex
      >>> is_s_dismantlable_vertex(nx.circulant_graph(7, [1, 2]), 0)
      True
      >>> is_dominated_vertex(nx.circulant_graph(7, [1, 2]), 0)
      False
      >>> is_s_dismantlable_vertex(nx.cycle_graph(4), 0)
      False

    """
    return is_dismantlable(open_neighborhood(graph, v))


def has_s_dismantlable_vertex(graph):
    """Returns whether a graph has s-dismantlable vertices

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      If the graph has dominated vertices, returns a list which only element
      is the first s-dismantlable vertex. Otherwise, return False

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import has_s_dismantlable_vertex
      >>> has_s_dismantlable_vertex(nx.circulant_graph(7, [1, 2]))
      [0]
      >>> has_s_dismantlable_vertex(nx.cycle_graph(4))
      False

    """
    for v in graph:
        if is_s_dismantlable_vertex(graph, v):
            return [v]
    else:
        return False


def remove_s_dismantlable_vertex(graph):
    """If a graph has an s-dismantlable vertex, returns a graph without it

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      If the graph has s-dismantlable vertices, returns a graph
      with the first s-dismantlable vertex removed. Otherwise, returns
      a copy of graph.

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import remove_s_dismantlable_vertex
      >>> g1 = remove_s_dismantlable_vertex(nx.circulant_graph(7, [1, 2]))
      >>> list(g1.nodes())
      [1, 2, 3, 4, 5, 6]

    """
    graph_aux = copy.deepcopy(graph)
    x = has_s_dismantlable_vertex(graph)
    if not x:
        return graph_aux
    else:
        graph_aux.remove_node(x[0])
        return graph_aux


def complete_s_collapse(graph):
    """Successively remove all s-dismantlable vertices from a graph

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      A graph obtained by successively removing s-dismantlable vertices

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import complete_s_collapse
      >>> g1 = complete_s_collapse(nx.circulant_graph(7, [1, 2]))
      >>> list(g1.nodes())
      [1, 3, 5, 6]

    """
    graph_aux = copy.deepcopy(graph)
    while True:
        n = graph_aux.order()
        graph_aux = remove_s_dismantlable_vertex(graph_aux)
        if n == graph_aux.order():
            return graph_aux


def is_s_dismantlable_edge(graph, e):
    """Returns whether an edge in a graph is s-dismantlable

    Args:
      graph (networkx.classes.graph.Graph): graph
      v: vertex in a graph

    Returns:
      True if the edge e is s-dismantlable in graph, False otherwise.

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import is_s_dismantlable_edge
      >>> is_s_dismantlable_edge(nx.complete_graph(3), (0, 1))
      True
      >>> is_s_dismantlable_edge(nx.cycle_graph(4), (0, 1))
      False

    """
    inter = graph.subgraph(set(graph[e[0]]).intersection(graph[e[1]])).copy()
    return is_dismantlable(inter)


def has_s_dismantlable_edge(graph):
    """Returns whether a graph has s-dismantlable edges

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      If the graph has a dismantlable_edge, returns the first that is found.
       Otherwise, return False

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import has_s_dismantlable_edge
      >>> has_s_dismantlable_edge(nx.complete_graph(3))
      (0, 1)
      >>> has_s_dismantlable_edge(nx.cycle_graph(4))
      False

    """
    for e in graph.edges():
        if is_s_dismantlable_edge(graph, e):
            return e
    else:
        return False


def remove_s_dismantlable_edge(graph):
    """If a graph has an s-dismantlable edge, returns a graph without it

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      If the graph has s-dismantlable edges, returns a graph
      with the first s-dismantlable edge removed. Otherwise, returns
      a copy of graph.

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import remove_s_dismantlable_edge
      >>> g1 = remove_s_dismantlable_edge(nx.complete_graph(3))
      >>> list(g1.edges())
      [(0, 2), (1, 2)]

    """
    graph_aux = copy.deepcopy(graph)
    x = has_s_dismantlable_edge(graph)
    if not x:
        return graph_aux
    else:
        graph_aux.remove_edge(*x)
        return graph_aux


def complete_s_collapse_edges(graph):
    """Successively remove all s-dismantlable edges from a graph

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      A graph obtained by succesively removing s-dismantlable edges

    Example:
      >>> import networkx as nx
      >>> from pycliques.dominated import complete_s_collapse_edges
      >>> g1 = complete_s_collapse_edges(nx.complete_graph(4))
      >>> list(g1.edges())
      [(0, 3), (1, 3), (2, 3)]

    """
    graph_aux = copy.deepcopy(graph)
    while True:
        n = graph_aux.size()
        graph_aux = remove_s_dismantlable_edge(graph_aux)
        if n == graph_aux.size():
            return graph_aux
