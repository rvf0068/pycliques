import networkx as nx
from pycliques.surfaces import open_neighborhood


def local_cutpoints(graph):
    for v in graph:
        if not nx.is_connected(open_neighborhood(graph, v)):
            yield v


def has_local_cutpoints(graph):
    try:
        cutpoints = local_cutpoints(graph)
        return [next(cutpoints)]
    except StopIteration:
        return False
