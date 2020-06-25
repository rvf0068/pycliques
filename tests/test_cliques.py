#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycliques.helly import is_clique_helly
import networkx as nx

__author__ = "Rafael Villarroel"
__copyright__ = "Rafael Villarroel"
__license__ = "mit"


octa = nx.octahedral_graph()
path5 = nx.path_graph(5)
cyc3 = nx.cycle_graph(3)


def test_is_clique_helly():
    assert not is_clique_helly(octa)
    assert is_clique_helly(path5)
    assert is_clique_helly(cyc3)
