import argparse
import sys
import logging
from pycliques import __version__
from pycliques.cliques import clique_graph
from pycliques.helly import is_helly
from pycliques.dominated import has_dominated_vertex
import networkx as nx
import pkg_resources

__author__ = "Rafael Villarroel"
__copyright__ = "Rafael Villarroel"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Clique behavior of small graphs")
    parser.add_argument(
        '--version',
        action='version',
        version='pycliques {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="n",
        help="order of graphs considered",
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
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


graph6c = pkg_resources.resource_filename('pycliques', '/data/graph6c.g6')
graph7c = pkg_resources.resource_filename('pycliques', '/data/graph7c.g6')
graph8c = pkg_resources.resource_filename('pycliques', '/data/graph8c.g6')
graph9c = pkg_resources.resource_filename('pycliques', '/data/graph9c.g6')
list6 = nx.read_graph6(graph6c)
list7 = nx.read_graph6(graph7c)
list8 = nx.read_graph6(graph8c)
# list9 = nx.read_graph6(graph9c)
dict_small = {6: list6, 7: list7, 8: list8}


def is_eventually_helly(g):
    i = 0
    while not is_helly(g) and i < 8:
        i = i+1
        g = clique_graph(g, 30)
        if g is None:
            return False
    return True


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    calculations = {}
    further_study = []
    all_graphs = dict_small[args.n]
    total = len(all_graphs)
    _logger.info("There are {} graphs of order {}".format(total, args.n))
    for index in range(total):
        _logger.debug("Considering graph with index {}".format(index))
        graph = all_graphs[index]
        if has_dominated_vertex(graph):
            calculations[index] = "Dominated vertex"
        elif is_eventually_helly(graph):
            calculations[index] = "Eventually Helly"
        else:
            calculations[index] = "Unknown so far"
            further_study.append(index)
        _logger.debug("Graph {}".format(calculations[index]))
    print("Indices that deserve further study: {}".format(further_study))
    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
