"""This files defines functions that study the Helly property."""
import networkx as nx


def triangles(g):
    vs = list(g.nodes())
    for v in vs:
        for u in [u for u in g[v] if vs.index(u) > vs.index(v)]:
            for w in [w for w in nx.common_neighbors(g, v, u)
                      if vs.index(w) > vs.index(u)]:
                yield [v, u, w]


def extended_triangle(g, t):
    a, b, c = t
    extt = t
    extt.extend(nx.common_neighbors(g, a, b))
    extt.extend(nx.common_neighbors(g, b, c))
    extt.extend(nx.common_neighbors(g, a, c))
    return g.subgraph(extt)


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
      >>> from pycliques.helly import is_helly
      >>> from pycliques.named import octa, cyc3
      >>> is_helly(octa)
      False
      >>> is_helly(cyc3)
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
