import networkx as nx
from networkx.algorithms import tournament
from itertools import chain, combinations
from functools import reduce
import math


class Simplex(frozenset):
    """A simplex."""
    def __new__(cls, elements):
        return super().__new__(cls, elements)

    def __repr__(self):
        u = set(self)
        if len(u) == 0:
            return "{}"
        else:
            return f"{u}"

    def dimension(self):
        return len(self) - 1


class SimplicialComplex(object):
    """A SimplicialComplex is composed of a set of vertices, and a set of
    simplices (of type Simplex), which correspond to subsets of the set of
    vertices.

    """
    def __init__(self, vertex_set, facet_set=None, function=None):
        self.vertex_set = set(vertex_set)
        self.facet_set = facet_set
        self.function = function

        def is_simplex(s):
            for facet in facet_set:
                if s <= facet:
                    return True
            else:
                return False

        def facet_set_from_function(complex):
            if complex.function(complex.vertex_set):
                return {Simplex(complex.vertex_set)}
            else:
                x = list(complex.vertex_set)[0]
                linkmax = facet_set_from_function(complex.link(x))
                fromlink = {Simplex(sigma.union({x})) for sigma in linkmax}
                delmax = facet_set_from_function(complex.deletion(x))
                fixdelmax = set()
                for delm in delmax:
                    for linkm in linkmax:
                        if delm <= linkm:
                            break
                    else:
                        fixdelmax.add(Simplex(delm))
                return fromlink.union(fixdelmax)

        if self.function is None:
            self.function = is_simplex

        if self.facet_set is None:
            self.facet_set = facet_set_from_function(self)
        else:
            self.facet_set = {Simplex(s) for s in self.facet_set}

    def __repr__(self):
        return f"Simplicial complex with vertex_set {self.vertex_set} and facets\
 {self.facet_set}."

    def __eq__(self, other):
        return self.vertex_set == other.vertex_set and \
            self.facet_set == other.facet_set

    def dimension(self):
        """The dimension of the simplicial complex."""
        d = -1
        for facet in self.facet_set:
            if facet.dimension() > d:
                d = facet.dimension()
        return d

    def deletion(self, x):
        def _new_function(s):
            return self.function(s) and x not in s

        new_vertices = self.vertex_set - {x}
        return SimplicialComplex(new_vertices, function=_new_function)

    def link(self, x):
        def _new_function(s):
            return self.function(s | {x})
        new_vertices = {y for y in self.vertex_set
                        if y != x and self.function({x, y})}
        return SimplicialComplex(new_vertices, function=_new_function)

    def skeleton(self, n):
        def _new_function(s):
            return self.function(s) and len(s) <= n+1
        return SimplicialComplex(self.vertex_set, function=_new_function)

    def one_skeleton_graph(self):
        """The 1-skeleton of the complex, but as a graph"""
        the_graph = nx.Graph()
        the_graph.add_nodes_from(self.vertex_set)
        pairs = combinations(self.vertex_set, 2)
        edges = [(i, j) for (i, j) in pairs if self.function({i, j})]
        the_graph.add_edges_from(edges)
        return the_graph

    def is_clique_complex(self):
        return self == clique_complex(self.one_skeleton_graph())

    def all_simplices(self):
        all = set([])
        for facet in self.facet_set:
            s = list(facet)
            all = all.union(set(chain.from_iterable(combinations(s, r)
                                                    for r in range(len(s)+1))))
        return {Simplex(s) for s in all}

    def dong_matching(self):
        matched = []
        vertices = list(self.vertex_set)
        for vertex in vertices:
            the_link = self.link(vertex)
            link_simplices = the_link.all_simplices()
            for s in link_simplices:
                if (s not in matched) and (not s | {vertex} in matched):
                    matched.append(s)
                    matched.append(s | {vertex})
        return self.all_simplices() - set(matched)


def nerve_of_sets(sets):
    def _non_empty_intersection(s):
        intersect = reduce(lambda x, y: x.intersection(y), list(s))
        return len(intersect) != 0
    vertices = [Simplex(s) for s in sets]
    return SimplicialComplex(vertices, function=_non_empty_intersection)


def clique_complex(graph):
    the_cliques = {Simplex(q) for q in nx.find_cliques(graph)}
    return SimplicialComplex(graph.nodes(), facet_set=the_cliques)


def nerve_of_cliques(graph):
    the_cliques = {frozenset(q) for q in nx.find_cliques(graph)}
    return nerve_of_sets(the_cliques)


def bounded_degree(graph, lambda_vector, list_of_edges):
    subgraph = graph.edge_subgraph(list_of_edges)
    for v in graph:
        if v in subgraph.nodes() and subgraph.degree(v) > lambda_vector[v]:
            return False
    else:
        return True


def bounded_degree_complex(graph, lambda_vector):
    def _bounded(s):
        return bounded_degree(graph, lambda_vector, s)
    return SimplicialComplex(graph.edges(), function=_bounded)


def is_oriented_simplex(digraph):
    return nx.is_directed_acyclic_graph(digraph) and \
        tournament.is_tournament(digraph)


def oriented_complex(digraph):
    def _oriented_simplex(s):
        return is_oriented_simplex(digraph.subgraph(s))
    return SimplicialComplex(digraph.nodes(), function=_oriented_simplex)


def complex_of_forests(graph, max_deg=math.inf):
    """The complex on the vertices of graph, where the simplices are subsets
    that induce a forest of maximum degree max_deg"""
    def _is_forest(s):
        subgraph = graph.subgraph(s)
        maxd = max([subgraph.degree(node) for node in subgraph.nodes])
        return nx.is_forest(graph.subgraph(s)) and maxd <= max_deg
    return SimplicialComplex(graph.nodes(), function=_is_forest)
