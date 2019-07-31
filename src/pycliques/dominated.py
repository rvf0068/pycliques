"""This files defines functions dealing with dominated vertices. A
vertex :math:`v` in a graph :math:`G` is a vertex such that there is
another vertex :math:`w` that..

"""
import copy

from pycliques.surfaces import open_neighborhood


def closed_neighborhood(g, v):
    return set(g[v]) | {v}


def is_dominated_vertex(g, v):
    for u in g:
        if u != v:
            if closed_neighborhood(g, v).issubset(closed_neighborhood(g, u)):
                return True
    else:
        return False


def has_dominated_vertex(g):
    for v in g:
        if is_dominated_vertex(g, v):
            return [v]
    else:
        return False


def remove_dominated_vertex(g):
    g1 = copy.deepcopy(g)
    x = has_dominated_vertex(g)
    if not x:
        return g1
    else:
        g1.remove_node(x[0])
        return g1


def completely_pared_graph(g):
    g1 = copy.deepcopy(g)
    while True:
        n = g1.order()
        g1 = remove_dominated_vertex(g1)
        if n == g1.order():
            return g1


def is_dismantlable(graph):
    return completely_pared_graph(graph).order() == 1


def is_s_dismantlable_vertex(graph, v):
    return is_dismantlable(open_neighborhood(graph, v))


def has_s_dismantlable_vertex(graph):
    for v in graph:
        if is_s_dismantlable_vertex(graph, v):
            return [v]
    else:
        return False


def remove_s_dismantlable_vertex(graph):
    graph_aux = copy.deepcopy(graph)
    x = has_s_dismantlable_vertex(graph)
    if not x:
        return graph_aux
    else:
        graph_aux.remove_node(x[0])
        return graph_aux


def complete_s_collapse(graph):
    graph_aux = copy.deepcopy(graph)
    while True:
        n = graph_aux.order()
        graph_aux = remove_s_dismantlable_vertex(graph_aux)
        if n == graph_aux.order():
            return graph_aux


def is_s_dismantlable_edge(graph, e):
    inter = graph.subgraph(set(graph[e[0]]).intersection(graph[e[1]])).copy()
    return is_dismantlable(inter)


def has_s_dismantlable_edge(graph):
    for e in graph.edges():
        if is_s_dismantlable_edge(graph, e):
            return e
    else:
        return False


def remove_s_dismantlable_edge(graph):
    graph_aux = copy.deepcopy(graph)
    x = has_s_dismantlable_edge(graph)
    if not x:
        return graph_aux
    else:
        graph_aux.remove_edge(*x)
        return graph_aux


def complete_s_collapse_edges(graph):
    graph_aux = copy.deepcopy(graph)
    while True:
        n = graph_aux.size()
        graph_aux = remove_s_dismantlable_edge(graph_aux)
        if n == graph_aux.size():
            return graph_aux
