import networkx as nx


class SimplicialComplex(object):
    """Documentation for SimplicialComplex

    """
    def __init__(self, vertex_set, facet_list=[], function=None):
        self.vertex_set = set(vertex_set)
        self.facet_list = facet_list
        self.function = function

    def __repr__(self):
        return f"Complex with vertex_set {self.vertex_set} and facets {self.facet_list}"

    def dimension(self):
        d = 0
        for facet in self.facet_list:
            if len(facet) > d:
                d = len(facet)
        return d

    def deletion(self, x):
        new_vertices = self.vertex_set - {x}
        if self.function:
            return SimplicialComplex(new_vertices, self.function)


def clique_complex(graph):
    the_cliques = list(nx.find_cliques(graph))
    return SimplicialComplex(graph.nodes(), facet_list=the_cliques)
