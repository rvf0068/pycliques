import networkx as nx
from itertools import chain, combinations


class SimplicialComplex(object):
    """A SimplicialComplex is composed of a set of vertices, and a set of
    frozensets, which are subsets of the set of vertices.

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
            if complex.vertex_set == set():
                return {frozenset()}
            elif complex.function(complex.vertex_set):
                return {frozenset(complex.vertex_set)}
            else:
                x = list(complex.vertex_set)[0]
                linkmax = facet_set_from_function(complex.link(x))
                fromlink = {sigma.union({x}) for sigma in linkmax}
                delmax = facet_set_from_function(complex.deletion(x))
                fixdelmax = set()
                for delm in delmax:
                    for linkm in linkmax:
                        if delm <= linkm:
                            break
                    else:
                        fixdelmax.add(delm)
                return fromlink.union(fixdelmax)

        if self.function is None:
            self.function = is_simplex

        if self.facet_set is None:
            self.facet_set = facet_set_from_function(self)

    def __repr__(self):
        return f"Simplicial complex with vertex_set {self.vertex_set} and facets\
 {self.facet_set}."

    def dimension(self):
        d = 0
        for facet in self.facet_set:
            if len(facet) > d:
                d = len(facet)
        return d

    def deletion(self, x):
        def _new_function(s):
            return self.function(s) and x not in s

        new_vertices = self.vertex_set - {x}
        return SimplicialComplex(new_vertices, function=_new_function)

    def link(self, x):
        def _new_function(s):
            return self.function(s | {x})
        new_vertices = set([y for y in self.vertex_set
                            if y != x and self.function({x, y})])
        return SimplicialComplex(new_vertices, function=_new_function)

    def skeleton(self, n):
        def _new_function(s):
            return self.function(s) and len(s) <= n+1
        return SimplicialComplex(self.vertex_set, function=_new_function)

    def all_simplices(self):
        all = set([])
        for facet in self.facet_set:
            s = list(facet)
            all = all.union(set(chain.from_iterable(combinations(s, r)
                                                    for r in range(len(s)+1))))
        return {frozenset(s) for s in all}

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


def clique_complex(graph):
    the_cliques = set([frozenset(q) for q in nx.find_cliques(graph)])
    return SimplicialComplex(graph.nodes(), facet_set=the_cliques)


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
    out_ok = False
    in_ok = False
    for v in digraph.nodes():
        if digraph.out_degree(v) == digraph.order()-1:
            out_ok = True
        if digraph.in_degree(v) == digraph.order()-1:
            in_ok = True
    return out_ok and in_ok


def oriented_complex(digraph):
    def _oriented_simplex(s):
        return is_oriented_simplex(digraph.subgraph(s))
    return SimplicialComplex(digraph.nodes(), function=_oriented_simplex)
