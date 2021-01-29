from networkx import nx
import itertools


def is_visible(y, a, b):
    isit = True
    c = a + 1
    while isit and c < b:
        isit = y[c] < y[b]+(y[a]-y[b])*((b-c)/float(b-a))
        c = c + 1
    return isit


def visibility_graph(time_series, directed=False):
    if directed:
        V = nx.DiGraph()
    else:
        V = nx.Graph()
    n = len(time_series)
    pairs = itertools.combinations(range(n), 2)
    V.add_edges_from((a, b) for (a, b) in pairs
                     if is_visible(time_series, a, b))
    return V
