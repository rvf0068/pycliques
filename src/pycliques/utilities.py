import argparse
import sys
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


def _parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Extract graphs from g6 file. Usage: extract_graphs -ff 'file.g6.gz' -l 2 10 200 -tf 'outfile.g6'")
    parser.add_argument(
        '-ff',
        '--from-file',
        dest="from_file",
        help="From file",
        type=str)
    parser.add_argument(
        '-l',
        '--list',
        nargs='+',
        dest="the_list",
        type=int,
        help="List of graphs")
    parser.add_argument(
        '-tf',
        '--to-file',
        dest="the_file",
        help="To file",
        type=str)
    return parser.parse_args(args)


def extract_graphs_from_file(from_file, the_list, the_file):
    index = 0
    with gzip.open(from_file, 'rt') as graph_file:
        with open(the_file, 'w') as extracted_graphs:
            for graph in graph_file:
                if index in the_list:
                    extracted_graphs.write(graph)
                index = index+1
    print(the_list)


def _main(args):
    args = _parse_args(args)
    extract_graphs_from_file(args.from_file, args.the_list, args.the_file)


def _run():
    """Entry point for console_scripts
    """
    _main(sys.argv[1:])


if __name__ == "__main__":
    _run()
