"""
A collection :math:`\mathcal{C}` of subsets of a set :math:`X` is called
*intersecting* if the intersection of any two elements of
:math:`\mathcal{C}` is non empty. The collection :math:`\mathcal{C}` is called
*Helly* if any intersecting subcollection :math:`\mathcal{C}'` of
:math:`\mathcal{C}` has non empty intersection. A graph is called *Helly*
if the collection of its cliques is Helly.
"""
from pycliques.dominated import is_dismantlable


def n_closed(graph, edge):
    return n_open(graph, edge) | set(edge)


def u_closed(graph, edge):
    subgraph = graph.subgraph(n_closed(graph, edge))
    return {v for v in subgraph if subgraph.degree(v) == subgraph.order()-1}


def u_closed_dict(graph):
    return {edge: u_closed(graph, edge) for edge in graph.edges()}


def n_open(graph, edge):
    return set(graph[edge[0]]) & set(graph[edge[1]])


def u_open(graph, edge):
    subgraph = graph.subgraph(n_open(graph, edge))
    return {v for v in subgraph if subgraph.degree(v) == subgraph.order()-1}


def u_open_dict(graph):
    return {edge: u_open(graph, edge) for edge in graph.edges()}


def is_clique_helly(graph):
    """Checks whether the graph is Helly

    Parameters
    ----------
    graph : NetworkX graph

    Returns
    -------
    bool
       True if the graph is Helly, False otherwise

    Notes
    -----
    This implementation is from [1]_.

    Examples
    --------
    >>> import networkx as nx
    >>> from pycliques.helly import is_clique_helly
    >>> is_clique_helly(nx.octahedral_graph())
    False
    >>> is_clique_helly(nx.cycle_graph(3))
    True

    References
    ----------
    .. [1] Lin, M. C., & Szwarcfiter, J. L., Faster recognition of clique-Helly
       and hereditary clique-Helly graphs, Information Processing Letters,
       103(1), 40–43 (2007).

    """
    edges = graph.edges()
    uclosed = u_closed_dict(graph)
    for e in edges:
        for v in n_open(graph, e):
            gooda = (e[0], v) if (e[0], v) in uclosed else (v, e[0])
            goodb = (e[1], v) if (e[1], v) in uclosed else (v, e[1])
            Sc = uclosed[gooda] & uclosed[goodb]
            if len(Sc & uclosed[e]) == 0:
                return False
    return True


def is_hereditary_clique_helly(graph):
    """Checks whether the graph is hereditary clique-Helly

    Parameters
    ----------
    graph : NetworkX graph

    Returns
    -------
    bool
       True if the graph is hereditary clique-Helly, False otherwise

    Notes
    -----
    This implementation is from [1]_.

    Examples
    --------
    >>> import networkx as nx
    >>> from pycliques.helly import is_hereditary_clique_helly
    >>> is_hereditary_clique_helly(nx.octahedral_graph())
    False
    >>> is_hereditary_clique_helly(nx.cycle_graph(3))
    True

    References
    ----------
    .. [1] Lin, M. C., & Szwarcfiter, J. L., Faster recognition of clique-Helly
       and hereditary clique-Helly graphs, Information Processing Letters,
       103(1), 40–43 (2007).

    """
    edges = graph.edges()
    uopen = u_open_dict(graph)
    for e in edges:
        for v in n_open(graph, e):
            gooda = (e[0], v) if (e[0], v) in uopen else (v, e[0])
            goodb = (e[1], v) if (e[1], v) in uopen else (v, e[1])
            if v not in uopen[e] and e[1] not in uopen[gooda] and \
               e[0] not in uopen[goodb]:
                return False
    return True


def is_disk_helly(graph):
    return is_dismantlable(graph) and is_clique_helly(graph)
