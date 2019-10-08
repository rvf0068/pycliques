import networkx as nx
from networkx.algorithms import isomorphism

import logging
import argparse
import sys

from pycliques import __version__
from pycliques.dominated import closed_neighborhood, completely_pared_graph
from pycliques.cliques import clique_graph
from pycliques.named import suspension_of_cycle, complement_of_cycle, \
    octahedron
from pycliques.utilities import dict_to_tuple, invert_dict
from pycliques.coaffinations import automorphisms


_logger = logging.getLogger(__name__)


def _parse_args(args):
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
        dest="large",
        help="large graph in g6 format",
        type=str,
        metavar="STR")
    parser.add_argument(
        dest="small",
        help="small graph in g6 format",
        type=str,
        metavar="STR")

    return parser.parse_args(args)


def _setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def is_map(domain, codomain, ismap):
    """
    Determine if a dictionary defines a graph map.

    It is not required that the every vertex in domain has a value
    determined in ismap.

    Args:
      domain (networkx.classes.graph.Graph): graph
      codomain (networkx.classes.graph.Graph): graph
      ismap ([dict]): map

    Returns:
      True if ismap defines a graph map, False otherwise.

    Example:
      >>> import networkx as nx
      >>> from pycliques.retractions import is_map
      >>> map = {0:0, 1:1, 2:0, 3:1}
      >>> is_map(nx.cycle_graph(4), nx.complete_graph(2), map)
      True
      >>> map = {0:0, 1:1}
      >>> is_map(nx.cycle_graph(4), nx.complete_graph(2), map)
      True

    """
    for e in domain.edges():
        if e[0] in ismap and e[1] in ismap:
            w1 = ismap[e[0]]
            w2 = ismap[e[1]]
            if not(codomain.has_edge(w1, w2)) and w1 != w2:
                return False
    else:
        return True


def _extension_of_map(large, small, mapp, v):
    """Given the graphs ``large``, ``small``, a (partial) map ``mapp``
    between them, and a vertex ``v`` of the graph ``large``, this
    function returns the set of vertices of the graph ``small`` that
    could be images of ``v`` under ``mapp``.
    """
    common = set(small.nodes())
    for w in large[v] & mapp.keys():
        common = common & closed_neighborhood(small, mapp[w])
    return common


def _extend_retraction(large, small, state):
    """We are given the graphs ``large`` and ``small``. Here ``state`` is
    a tuple of pairs, that defines a (partial) map from ``large`` to
    ``small``. This function uses backtracking to complete a
    retraction from ``large`` to ``small``.
    """
    ret = dict(state)
    remaining = list(large.nodes()-ret.keys())
    _logger.info("Remaining: {}".format(remaining))
    for v in remaining:
        for w in _extension_of_map(large, small, ret, v):
            if len(ret) == len(large)-1:
                yield ((v, w),)
            else:
                for res in _extend_retraction(large, small, state+((v, w),)):
                    yield ((v, w),)+res


def retraction(large, small):
    """Generator of retractions from large to small.

    Args:
      large (networkx.classes.graph.Graph): graph
      small (networkx.classes.graph.Graph): graph

    Returns:
      A generator of the retractions from a graph to other.

      A retraction is given as a pair of dictionaries, the first
      defines a map from large to small and the second defines a
      a map from the small to the large (this is an inclusion).
      The composition of the second map with the first has to be
      the identity.

    Example:
      >>> import networkx as nx
      >>> from pycliques.retractions import retraction
      >>> list(retraction(nx.wheel_graph(4), nx.cycle_graph(4)))
      []
      >>> list(retraction(nx.path_graph(3), nx.path_graph(2)))
      [({0: 0, 1: 1, 2: 0}, {0: 0, 1: 1}), ({0: 0, 1: 1, 2: 1}, {0: 0, 1: 1})]

    """
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    a_small = list(automorphisms(small))
    a_large = list(automorphisms(large))
    all_autos = [(auto_s, auto_l) for auto_s in a_small for auto_l in a_large]
    repeated = []
    for ret in rets:
        if ret not in repeated:
            if large.order() == small.order():
                yield (ret, invert_dict(ret))
            else:
                state = dict_to_tuple(ret)
                _logger.info("So far: {}".format(state))
                extension = _extend_retraction(large, small, state)
                for ext in extension:
                    yield (dict(state+ext), invert_dict(ret))
            for auto_s, auto_l in all_autos:
                new_repeated = dict([(auto_l[x], auto_s[ret[x]]) for x in ret])
                repeated.append(new_repeated)


def retracts(large, small):
    """Whether the graph large retracts to small

    Args:
      large (networkx.classes.graph.Graph): graph
      small (networkx.classes.graph.Graph): graph

    Returns:
      If there is a retraction from large to small, return it.
      Otherwise, return False.

   Example:
      >>> import networkx as nx
      >>> from pycliques.retractions import retracts
      >>> retracts(nx.wheel_graph(5), nx.cycle_graph(4))
      False
      >>> retracts(nx.path_graph(3), nx.path_graph(2))
      ({0: 0, 1: 1, 2: 0}, {0: 0, 1: 1})

    """
    try:
        rets = retraction(large, small)
        return next(rets)
    except StopIteration:
        return False


def retracts_to(subgraph):
    """Boolean function that gives the retraction to a subgraph

    Args:
      large (networkx.classes.graph.Graph): graph

    Returns:
      A boolean function that determines if its argument retracts to
      subgraph.

    Example:
      >>> import networkx as nx
      >>> from pycliques.retractions import retracts_to
      >>> retracts_to(nx.cycle_graph(4))(nx.wheel_graph(5))
      False
      >>> retracts_to(nx.path_graph(2))(nx.path_graph(3))
      ({0: 0, 1: 1, 2: 0}, {0: 0, 1: 1})

    """
    return lambda g: retracts(g, subgraph)


def has_induced(large, small):
    """Whether the graph large has an induced subgraph isomorphic to small

    Args:
      large (networkx.classes.graph.Graph): graph
      small (networkx.classes.graph.Graph): graph

    Returns:
      If large has a subgraph induced isomorphic to small, return the first
      inyective map from small to large found. Otherwise, return False.

      The map gives a correspondence from vertices in the large to small.

    Example:
      >>> import networkx as nx
      >>> from pycliques.retractions import has_induced
      >>> has_induced(nx.wheel_graph(5), nx.cycle_graph(4))
      {1: 0, 2: 1, 3: 2, 4: 3}
      >>> has_induced(nx.complete_graph(4), nx.cycle_graph(4))
      False

    """
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    try:
        return next(rets)
    except StopIteration:
        return False


def _string_to_graph(string):
    if string[0:2] == 'sc':
        return suspension_of_cycle(int(string[2:]))
    elif string[0:2] == "cc":
        return complement_of_cycle(int(string[2:]))
    elif string[0] == "o":
        return octahedron(int(string[1:]))


def _main(args):
    args = _parse_args(args)
    index = args.n
    _setup_logging(args.loglevel)
    large = nx.from_graph6_bytes(bytes(args.large, 'utf8'))
    small = _string_to_graph(args.small)
    for i in range(index):
        _logger.info("Iterating the clique operator")
        large = completely_pared_graph(clique_graph(large))
    large = nx.convert_node_labels_to_integers(large)
    _logger.info("The large graph has order {}".format(large.order()))
    _logger.info("Searching for retractions")
    has_retraction = retracts(large, small)
    if has_retraction:
        print("Found {}".format(has_retraction))
    else:
        print("Sorry, could not find it!")
    _logger.info("Script ends here")


def _run():
    """Entry point for console_scripts
    """
    _main(sys.argv[1:])


if __name__ == "__main__":
    _run()
