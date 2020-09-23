import networkx as nx


class SimplicialComplex(object):
    """Documentation for SimplicialComplex

    """
    def __init__(self, vertices, facet_list=[], function=None):
        self.vertices = vertices
        self.facet_list = facet_list
        self.function = function

    def __repr__(self):
        return f"Complex with vertices {self.vertices} and facets {self.facet_list}"

    def dimension(self):
        d = 0
        for facet in self.facet_list:
            if len(facet) > d:
                d = len(facet)
        return d


def clique_complex(graph):
    the_cliques = list(nx.find_cliques(graph))
    return SimplicialComplex(graph.nodes(), the_cliques)
