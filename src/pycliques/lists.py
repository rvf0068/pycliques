"""
This file gives an interface to use graph data from
Brendan McKay's `page
<http://cs.anu.edu.au/~bdm/data/graphs.html>`_. Currently only
includes the data for connected graphs from 6 to 10 vertices.

"""

import networkx as nx

import pkg_resources
import gzip

graph6c = pkg_resources.resource_filename('pycliques', '/data/graph6c.g6.gz')
graph7c = pkg_resources.resource_filename('pycliques', '/data/graph7c.g6.gz')
graph8 = pkg_resources.resource_filename('pycliques', '/data/graph8.g6.gz')
graph8c = pkg_resources.resource_filename('pycliques', '/data/graph8c.g6.gz')
graph9 = pkg_resources.resource_filename('pycliques', '/data/graph9.g6.gz')
graph9c = pkg_resources.resource_filename('pycliques', '/data/graph9c.g6.gz')
graph10 = pkg_resources.resource_filename('pycliques', '/data/graph10.g6.gz')
graph10c = pkg_resources.resource_filename('pycliques', '/data/graph10c.g6.gz')
_dict_all = {8: graph8, 9: graph9, 10: graph10}
_dict_connected = {6: graph6c, 7: graph7c, 8: graph8c, 9: graph9c,
                   10: graph10c}


def list_graphs(n, connected=True):
    """List of connected graphs of a given order, from B. McKay data

    Args:
      n (int): integer. Only supported between 6 and 10

    Returns:
      list: List of NetworkX graphs

    Examples:
      >>> from pycliques.lists import list_graphs
      >>> len(list_graphs(6))
      112

    """
    list_of_graphs = []
    if connected:
        the_dict = _dict_connected
    else:
        the_dict = _dict_all
    with gzip.open(the_dict[n], 'rt') as graph_file:
        for graph in graph_file:
            graph = graph.strip()
            graph = nx.from_graph6_bytes(bytes(graph, 'utf8'))
            list_of_graphs.append(graph)
    return list_of_graphs
