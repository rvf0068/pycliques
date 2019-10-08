import argparse
import sys
import logging
import gzip

import networkx as nx

from pycliques import __version__
from pycliques.cliques import clique_graph
from pycliques.helly import is_helly
from pycliques.dominated import has_dominated_vertex, completely_pared_graph
from pycliques.special import special_octahedra
from pycliques.retractions import retracts, retracts_to
from pycliques.named import suspension_of_cycle, complement_of_cycle
from pycliques.lists import _dict_small


__author__ = "Rafael Villarroel"
__copyright__ = "Rafael Villarroel"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def _parse_args(args):
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


def _setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def is_eventually_helly(g):
    i = 0
    while not is_helly(g) and i < 8:
        i = i+1
        g = clique_graph(g, 30)
        if g is None:
            return False
        else:
            g = completely_pared_graph(g)
    if is_helly(g):
        _logger.info("Helly of index {}".format(i))
        return True
    else:
        return False


def eventually_retracts_specially(g):
    i = 0
    while i < 8 and not special_octahedra(g):
        i = i+1
        g = clique_graph(g, 20)
        if g is None:
            return False
        else:
            g = completely_pared_graph(g)
    if i == 8:
        return False
    else:
        _logger.info("Index {} has induced special octahedra".format(i))
        return True


def retracts_to_some_suspension_of_cycle(g, indices):
    for n in indices:
        if retracts(g, suspension_of_cycle(n)):
            return n
    else:
        return False


def retracts_to_some_complement_of_cycle(g, indices):
    for n in indices:
        if retracts(g, complement_of_cycle(n)):
            return n
    else:
        return False


def _main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = _parse_args(args)
    _setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    calculations = {}
    further = []
    all_graphs = _dict_small[args.n]
    index = 0
    with gzip.open(all_graphs, 'rt') as graph_file:
        for graph in graph_file:
            graph = graph.strip()
            graph = nx.from_graph6_bytes(bytes(graph, 'utf8'))
            _logger.debug("Considering graph with index {}".format(index))
            if has_dominated_vertex(graph):
                calculations[index] = "has a dominated vertex"
            elif is_eventually_helly(graph):
                calculations[index] = "is eventually Helly"
            elif special_octahedra(graph):
                calculations[index] = "has an induced special octahedron"
            elif retracts_to(suspension_of_cycle(5))(graph):
                calculations[index] = "retracts to Susp(C_5)"
            elif retracts_to(suspension_of_cycle(6))(graph):
                calculations[index] = "retracts to Susp(C_6)"
            elif retracts_to(complement_of_cycle(8))(graph):
                calculations[index] = "retracts to Comp(C_8)"
            elif eventually_retracts_specially(graph):
                calculations[index] = "eventually has a special octahedron"
            else:
                calculations[index] = "has character unknown so far"
                further.append(index)
            _logger.debug("This graph {}".format(calculations[index]))
            index = index + 1
    _logger.info("Indices that deserve further study: {}".format(further))
    _logger.info("Script ends here")


def _run():
    """Entry point for console_scripts
    """
    _main(sys.argv[1:])


if __name__ == "__main__":
    _run()
