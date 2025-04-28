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

small_torsion = pkg_resources.resource_filename(
    'pycliques', '/data/small-torsion.g6'
)


def graph_generator(n, connected=True):
    """
    Yields NetworkX graphs from a g6.gz file.

    Args:
        n (int): Order of the graphs (number of nodes). Supported: 6 to 10.
        connected (bool): If True, reads connected graphs file; else,
            reads all graphs file. Defaults to True.

    Yields:
        nx.Graph: A NetworkX graph read from the file.

    Examples:
        >>> from pycliques.lists import graph_generator
        >>> generator = graph_generator(6)
        >>> graph = next(generator)
        >>> type(graph)
        <class 'networkx.classes.graph.Graph'>
    """
    if connected:
        the_dict = _dict_connected
    else:
        the_dict = _dict_all

    file_path = the_dict[n]

    with gzip.open(file_path, 'rt') as graph_file:
        for graph_string in graph_file:
            graph_string = graph_string.strip()
            graph = nx.from_graph6_bytes(bytes(graph_string, 'utf8'))
            yield graph


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
    return list(graph_generator(n, connected))


def small_torsion_graphs():
    list_of_graphs = []
    with open(small_torsion, 'r') as graph_file:
        for graph in graph_file:
            graph = graph.strip()
            graph = nx.from_graph6_bytes(bytes(graph, 'utf8'))
            list_of_graphs.append(graph)
    return list_of_graphs
