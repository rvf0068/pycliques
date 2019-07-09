import networkx as nx

import pkg_resources
import gzip

graph6c = pkg_resources.resource_filename('pycliques', '/data/graph6c.g6.gz')
graph7c = pkg_resources.resource_filename('pycliques', '/data/graph7c.g6.gz')
graph8c = pkg_resources.resource_filename('pycliques', '/data/graph8c.g6.gz')
graph9c = pkg_resources.resource_filename('pycliques', '/data/graph9c.g6.gz')
graph10c = pkg_resources.resource_filename('pycliques', '/data/graph10c.g6.gz')
_dict_small = {6: graph6c, 7: graph7c, 8: graph8c, 9: graph9c, 10: graph10c}


def enlist_graphs(n):
    list_of_graphs = []
    with gzip.open(_dict_small[n], 'rt') as graph_file:
        for graph in graph_file:
            graph = graph.strip()
            graph = nx.from_graph6_bytes(bytes(graph, 'utf8'))
            list_of_graphs.append(graph)
    return list_of_graphs
