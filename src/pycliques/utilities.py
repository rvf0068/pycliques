import gzip

import networkx as nx

from pycliques.lists import _dict_connected


def dict_to_tuple(the_dict):
    return tuple((a, b) for a, b in the_dict.items())


def invert_dict(the_dict):
    return dict((b, a) for a, b in the_dict.items())


def extract_graphs(the_list, order, the_file):
    index = 0
    translation = {}
    with gzip.open(_dict_connected[order], 'rt') as graph_file:
        with open(the_file, 'w') as extracted_graphs:
            for graph in graph_file:
                if index in the_list:
                    translation[index] = graph.strip()
                index = index+1
            extracted_graphs.write(str(translation))


def graph_from_gap_adjacency_list(the_list):
    graph = nx.Graph()
    for i, adj in enumerate(the_list):
        graph.add_edges_from([(i, v-1) for v in adj])
    return graph
