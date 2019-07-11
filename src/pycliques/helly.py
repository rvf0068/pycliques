"""This files defines functions that study the Helly property."""
import networkx as nx


def triangles(g):
    vs = list(g.nodes())
    for v in vs:
        for u in [u for u in g[v] if vs.index(u) > vs.index(v)]:
            for w in [w for w in nx.common_neighbors(g, v, u)
                      if vs.index(w) > vs.index(u)]:
                yield [v, u, w]


def extended_triangle(graph, triangle):
    vertex_a, vertex_b, vertex_c = triangle
    ext_triangle = triangle
    ext_triangle.extend(nx.common_neighbors(graph, vertex_a, vertex_b))
    ext_triangle.extend(nx.common_neighbors(graph, vertex_b, vertex_c))
    ext_triangle.extend(nx.common_neighbors(graph, vertex_a, vertex_c))
    return graph.subgraph(ext_triangle)


def is_cone(g):
    vs = g.nodes()
    n = g.order()
    for v in vs:
        if g.degree(v) == n-1:
            return True
    else:
        return False


def is_helly(g):
    """Checks whether the graph is Helly

    Args:
      g (networkx.classes.graph.Graph): graph

    Returns:
      bool: whether g is Helly

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
