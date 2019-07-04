import networkx as nx


def is_regular(graph, k):
    for v in graph:
        if not(graph.degree(v) == k):
            return False
    else:
        return True


def is_cycle(graph):
    return nx.is_connected(graph) and is_regular(graph, 2)


def is_path(graph):
    leaves = [x for x in graph if graph.degree(x) == 1]
    return nx.is_tree(graph) and len(leaves) == 2


def open_neighborhood(graph, v):
    return graph.subgraph(graph[v])


def is_closed_surface(graph):
    for v in graph:
        if not is_cycle(open_neighborhood(graph, v)):
            return False
    else:
        return True


def is_surface(graph):
    for v in graph:
        on = open_neighborhood(graph, v)
        if not is_cycle(on) and not is_path(on):
            return False
    else:
        return True
