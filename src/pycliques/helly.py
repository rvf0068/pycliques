"""
A collection :math:`\mathcal{C}` of subsets of a set :math:`X` is called
*intersecting* if the intersection of any two elements of
:math:`\mathcal{C}` is non empty. The collection :math:`\mathcal{C}` is called
*Helly* if any intersecting subcollection :math:`\mathcal{C}'` of
:math:`\mathcal{C}` has non empty intersection. A graph is called *Helly*
if the collection of its cliques is Helly.
"""

import networkx as nx


def triangles(graph):
    """Generator of the triangles in a graph

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      A generator of the triangles in a graph

    Example:
      >>> import networkx as nx
      >>> from pycliques.helly import triangles
      >>> list(triangles(nx.complete_graph(4)))
      [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]

    """
    vs = list(graph.nodes())
    for v in vs:
        for u in [u for u in graph[v] if vs.index(u) > vs.index(v)]:
            for w in [w for w in nx.common_neighbors(graph, v, u)
                      if vs.index(w) > vs.index(u)]:
                yield [v, u, w]


def extended_triangle(graph, triangle):
    """The extended triangle of a triangle in a graph

    Args:
      graph (networkx.classes.graph.Graph): graph
      triangle : a list of three vertices

    Returns:
      The subgraph of graph induced by the vertices that are neighbors
      to at least two vertices in the triangle.

    Example:
      >>> import networkx as nx
      >>> from pycliques.helly import extended_triangle
      >>> extended_triangle(nx.icosahedral_graph(), [0, 1, 5]).nodes()
      NodeView((0, 1, 5, 6, 8, 11))

    """
    vertex_a, vertex_b, vertex_c = triangle
    ext_triangle = triangle
    ext_triangle.extend(nx.common_neighbors(graph, vertex_a, vertex_b))
    ext_triangle.extend(nx.common_neighbors(graph, vertex_b, vertex_c))
    ext_triangle.extend(nx.common_neighbors(graph, vertex_a, vertex_c))
    return graph.subgraph(ext_triangle)


def is_cone(graph):
    """Returns whether the graph is a cone

    Args:
      graph (networkx.classes.graph.Graph): graph

    Returns:
      bool: True if there is a vertex in graph that is a neighbor of all
      other vertices, False otherwise

    Example:
      >>> import networkx as nx
      >>> from pycliques.helly import is_cone
      >>> is_cone(nx.wheel_graph(4))
      True
      >>> is_cone(nx.cycle_graph(4))
      False

    """
    for v in graph:
        if graph.degree(v) == graph.order()-1:
            return True
    else:
        return False


def is_helly(g):
    """Checks whether the graph is Helly

    Args:
      g (networkx.classes.graph.Graph): graph

    Returns:
      bool: True if the graph is Helly, False otherwise

    Examples:
      >>> import networkx as nx
      >>> from pycliques.helly import is_helly
      >>> is_helly(nx.octahedral_graph())
      False
      >>> is_helly(nx.cycle_graph(3))
      True

    """
    ite = triangles(g)
    while True:
        try:
            tri = next(ite)
            if not is_cone(extended_triangle(g, tri)):
                return False
        except StopIteration:
            return True
