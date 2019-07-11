import networkx as nx
from networkx.algorithms.operators.unary import complement

import itertools
import logging
import argparse
import sys


from pycliques import __version__
from pycliques.cliques import clique_graph
from pycliques.dominated import completely_pared_graph


_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Retractions to octahedra")
    parser.add_argument(
        '--version',
        action='version',
        version='pycliques {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="n",
        help="index of clique graph",
        type=int,
        metavar="INT")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        dest="graph_string",
        help="graph in g6 format",
        type=str,
        metavar="STR")
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def _adyacency_f(graph, edges):
    vertices = []
    for edge in edges:
        vertices.extend(edge)
    subgraph = graph.subgraph(vertices)
    for vertex in subgraph.nodes():
        if subgraph.degree(vertex) != 1:
            return False
    else:
        return True


def _is_clique(graph, clique):
    for v in graph:
        if not(v in clique):
            for w in clique:
                if not(graph.has_edge(v, w)):
                    break
            else:
                return False
    else:
        return True


def induced_octahedra(graph):
    c_graph = complement(graph)
    aux_graph = nx.Graph()
    edges_complement = c_graph.edges()
    aux_graph.add_nodes_from(edges_complement)
    _logger.info("The auxiliary graph has order {}".format(aux_graph.order()))
    pairs = itertools.combinations(edges_complement, 2)
    pairs = [(e1, e2) for (e1, e2) in pairs if _adyacency_f(c_graph, (e1, e2))]
    aux_graph.add_edges_from(pairs)
    cliques_aux = nx.find_cliques(aux_graph)
    octas = 0
    while True:
        try:
            edges_octa = next(cliques_aux)
            if len(edges_octa) >= 3:
                _logger.info("Trying octahedron {}".format(edges_octa))
                octas = octas+1
                vertices_octa = []
                for edge in edges_octa:
                    vertices_octa.extend(edge)
                octa = graph.subgraph(vertices_octa)
                cliques_octa = nx.find_cliques(octa)
                while True:
                    try:
                        clique_octa = next(cliques_octa)
                        _logger.info("Trying complete {}".format(clique_octa))
                        if _is_clique(graph, clique_octa):
                            print(octa.nodes, clique_octa)
                            return True
                    except StopIteration:
                        break
        except StopIteration:
            break
    _logger.info("No luck today. Tried {} octahedra".format(octas))
    return False


def main(args):
    args = parse_args(args)
    index = args.n
    setup_logging(args.loglevel)
    graph = nx.from_graph6_bytes(bytes(args.graph_string, 'utf8'))
    for i in range(index):
        _logger.info("Iterating the clique operator")
        graph = completely_pared_graph(clique_graph(graph))
    graph = nx.convert_node_labels_to_integers(graph)
    _logger.info("This graph has order {}".format(graph.order()))
    _logger.info("Searching for octahedra")
    has_induced = induced_octahedra(graph)
    if has_induced:
        print("Found it!")
    else:
        print("Sorry, could not find it!")
    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
