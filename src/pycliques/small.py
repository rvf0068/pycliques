import argparse
import sys
import logging
import gzip

import networkx as nx

from pycliques import __version__
from pycliques.cliques import clique_graph
from pycliques.helly import is_clique_helly
from pycliques.dominated import completely_pared_graph
from pycliques.special import special_octahedra
from pycliques.retractions import retracts, retracts_to
from pycliques.named import suspension_of_cycle, complement_of_cycle
from pycliques.lists import _dict_connected

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

__author__ = "Rafael Villarroel"
__copyright__ = "Rafael Villarroel"
__license__ = "mit"

_logger = logging.getLogger("rich")


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
        version=f'pycliques {__version__}')
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


def is_eventually_helly(graph, tries=8, bound=30):
    """Whether `graph` is eventually Helly

    Args:
      graph (networkx.classes.graph.Graph): graph
      tries : int
      bound : int

    Returns:
      True if an iterated clique graph with index less than `tries` of `graph`
      is Helly, in such a way that the order of an iterated clique graph
      is never greater than `bound`.

    Examples:
      >>> import networkx as nx
      >>> from pycliques.helly import is_clique_helly
      >>> from pycliques.small import is_eventually_helly
      >>> is_clique_helly(nx.triangular_lattice_graph(3,3))
      False
      >>> is_eventually_helly(nx.triangular_lattice_graph(3,3))
      True

    """
    i = 0
    while not is_clique_helly(graph) and i < tries:
        i = i+1
        graph = clique_graph(graph, bound)
        if graph is None:
            return False
        else:
            graph = completely_pared_graph(graph)
    if is_clique_helly(graph):
        _logger.info(f"Helly of index {i}")
        return True
    else:
        return False


def eventually_retracts_specially(graph, tries=8, bound=20):
    """Whether `graph` eventually retracts specially to an octahedron

    Args:
      graph (networkx.classes.graph.Graph): graph
      tries : int
      bound : int

    Returns:
      True if an iterated clique graph of `graph` with index less than `tries`
      retracts specially to an octahedron, in such a way that the order of
      all iterated clique graphs is always less than `bound`.

    Example:
      >>> from pycliques.lists import list_graphs
      >>> from pycliques.retractions import retracts
      >>> from pycliques.named import octahedron
      >>> from pycliques.small import eventually_retracts_specially
      >>> g = list_graphs(8)[11045]
      >>> retracts(g, octahedron(3))
      False
      >>> eventually_retracts_specially(g)
      True

    """

    i = 0
    while i < tries and not special_octahedra(graph):
        i = i+1
        graph = clique_graph(graph, bound)
        if graph is None:
            return False
        else:
            graph = completely_pared_graph(graph)
    if i == tries:
        return False
    else:
        _logger.info("Index {} has induced special octahedra".format(i))
        return True


def retracts_to_some_suspension_of_cycle(g, indices):
    """Whether the graph retracts to some suspension of a cycle"""

    for n in indices:
        if retracts(g, suspension_of_cycle(n)):
            return n
    else:
        return False


def retracts_to_some_complement_of_cycle(g, indices):
    """Whether the graph retracts to some complement of a cycle"""

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
    convergent = []
    divergent = []
    all_graphs = _dict_connected[args.n]
    index = 0
    with gzip.open(all_graphs, 'rt') as graph_file:
        for graph in graph_file:
            graph = graph.strip()
            graph = nx.from_graph6_bytes(bytes(graph, 'utf8'))
            _logger.debug("Considering graph with index {}".format(index))
            graph = completely_pared_graph(graph)
            if is_eventually_helly(graph):
                calculations[index] = "is eventually Helly"
                convergent.append(index)
            elif special_octahedra(graph):
                calculations[index] = "has an induced special octahedron"
                divergent.append(index)
            elif retracts_to(suspension_of_cycle(5))(graph):
                calculations[index] = "retracts to Susp(C_5)"
                divergent.append(index)
            elif retracts_to(suspension_of_cycle(6))(graph):
                calculations[index] = "retracts to Susp(C_6)"
                divergent.append(index)
            elif retracts_to(complement_of_cycle(8))(graph):
                calculations[index] = "retracts to Comp(C_8)"
                divergent.append(index)
            elif eventually_retracts_specially(graph):
                calculations[index] = "eventually has a special octahedron"
                divergent.append(index)
            else:
                calculations[index] = "has character unknown so far"
                further.append(index)
            _logger.debug(f"This graph {calculations[index]}")
            index = index + 1
    _logger.info(f"Indices that deserve further study: {further}")
    _logger.info(f"There are {len(convergent)} surely convergent graphs")
    _logger.info(f"There are {len(divergent)} surely divergent graphs")
    _logger.info("Script ends here")


def _run():
    """Entry point for console_scripts
    """
    _main(sys.argv[1:])


if __name__ == "__main__":
    _run()
