"""
This file defines a function for the clique graph. It is basically
the same as ``networkx.algorithms.clique.make_max_clique_graph``, but
includes a parameter to abort the construction in case the graph has
too many vertices.

For an undirected graph :math:`G`, its *clique graph* is defined as the
intersection graph of its maximal complete subgraphs.
"""

import networkx as nx
import numpy as np
import itertools
import math

from pycliques.coaffinations import CoaffinePair


class Clique(frozenset):
    """
    Base class for a clique in a graph.

    This class is derived from frozenset, but we modify its representation so
    that it does not print the word 'frozenset'.
    """
    def __repr__(self):
        u = set(self)
        if len(u) == 0:
            return "{}"
        else:
            return f"{u}"


def clique_graph(graph, bound=math.inf):
    """The clique graph operator

    Parameters
    ----------
    graph : NetworkX graph
            An undirected graph

    bound : int
            Upper bound accepted for order of clique graph

    Returns
    -------
    NetworkX graph
        the clique graph of graph

    Examples
    --------
    >>> import networkx as nx
    >>> from pycliques.cliques import clique_graph
    >>> g=clique_graph(nx.octahedral_graph())
    >>> g.nodes()
    NodeView(({0, 1, 2}, {0, 1, 3}, {0, 2, 4}, {0, 3, 4}, {1, 2, 5}, {1, 3, 5}, {2, 4, 5}, {3, 4, 5}))

    """
    if isinstance(graph, CoaffinePair):
        return _k_coaffine_pair(graph, bound)
    it_cliques = nx.find_cliques(graph)
    cliques = []
    K = nx.Graph()
    while True:
        try:
            clique = next(it_cliques)
            cliques.append(Clique(clique))
            if len(cliques) > bound:
                return None
        except StopIteration:
            break
    K.add_nodes_from(cliques)
    clique_pairs = itertools.combinations(cliques, 2)
    K.add_edges_from((c1, c2) for (c1, c2) in clique_pairs if c1 & c2)
    return K


def _k_coaffine_pair(pair, bound=math.inf):
    """The clique graph of a coaffine pair, as a coaffine pair."""
    g = pair.graph
    sigma = pair.coaffination
    kg = clique_graph(g, bound)
    coaf_k = dict([])
    for q in kg:
        coaf_k[q] = Clique([sigma[x] for x in q])
    return CoaffinePair(kg, coaf_k)


# pos is for the original graph
def pos_clique(clique_graph, pos, factor=1, bound=math.inf):
    """Generates a position dictionary for the clique graph

    Each vertex of the clique graph is assigned a position as the
    barycentric subdivision of the positions of the vertices of the
    clique.

    Parameters
    ----------
    clique_graph : NetworkX graph
        The graph whose cliques will get a coordinate
    pos : dict
        The dictionary of positions of vertices of the original graph
        (such as the output of `nx.spring_layout(graph)`)
    factor : float
        Factor for all positions
    bound : int
        Upper bound for the acceptable amount of vertices

    Examples
    --------
    >>> import networkx as nx
    >>> from pycliques.cliques import clique_graph as k
    >>> from pycliques.cliques import pos_clique
    >>> g = nx.cycle_graph(4)
    >>> pos = {0: [1, 0], 1: [0, 1], 2: [-1, 0], 3: [0, -1]}
    >>> pos_clique(k(g), pos)
    {{0, 1}: array([0.5, 0.5]), {0, 3}: array([ 0.5, -0.5]), {1, 2}: array([-0.5,  0.5]), {2, 3}: array([-0.5, -0.5])}

    """
    posK = dict()
    for clique in clique_graph:
        posK[clique] = factor*np.mean([pos[x] for x in clique], axis=0)
    return posK


def homotopy_clique_graph(graph):
    """The homotopy clique graph

    Parameters
    ----------
    graph : NetworkX graph
            An undirected graph

    Returns
    -------
    NetworkX graph
        the homotopy clique graph of graph

    Notes
    -----
    This is the operator :math:`H` defined in [3]_.

    References
    ----------
    .. [3] F. Larrión, M. A. Pizaña and R. Villarroel-Flores. Posets, clique
       graphs and their homotopy type. European Journal of Combinatorics,
       29(1), (2008) pp. 334-342.
    """

    def _ady(c1, c2):
        return (c1[0] in c2[1]) and (c2[0] in c1[1])
    H = nx.Graph()
    cliques = [Clique(q) for q in nx.find_cliques(graph)]
    vertices = [(x, q) for x in graph.nodes() for q in cliques if x in q]
    H.add_nodes_from(vertices)
    vertex_pairs = itertools.combinations(vertices, 2)
    H.add_edges_from((c1, c2) for (c1, c2) in vertex_pairs if _ady(c1, c2))
    return H
