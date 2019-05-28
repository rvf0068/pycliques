from pycliques.cliques import clique_graph
from pycliques.helly import is_helly
import networkx as nx
import pkg_resources

gr6 = pkg_resources.resource_filename('pycliques', '/data/graph6c.g6')
gr7 = pkg_resources.resource_filename('pycliques', '/data/graph7c.g6')
gr8 = pkg_resources.resource_filename('pycliques', '/data/graph8c.g6')
gr9 = pkg_resources.resource_filename('pycliques', '/data/graph9c.g6')
l6 = nx.read_graph6(gr6)
l7 = nx.read_graph6(gr7)
l8 = nx.read_graph6(gr8)
l9 = nx.read_graph6(gr9)


def is_eventually_helly(g):
    i = 0
    while not is_helly(g) and i < 8:
        i = i+1
        g = clique_graph(g, 30)
        if g is None:
            return False
    return True
