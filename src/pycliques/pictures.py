import random
from networkx.drawing.nx_agraph import graphviz_layout

import matplotlib.pyplot as plt

import networkx as nx
from networkx.generators.atlas import graph_atlas_g


def picture_list(criterion, the_list=graph_atlas_g()[1:208], fig_size=(4,4)):
    """Based on the code from
https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_atlas.html

    """
    U = nx.Graph()
    for G in the_list:
        if criterion(G):
            U = nx.disjoint_union(U, G)
    plt.figure(1, figsize=fig_size)
    pos = graphviz_layout(U, prog="neato")
    # color nodes the same in each connected subgraph
    C = (U.subgraph(c) for c in nx.connected_components(U))
    for g in C:
        c = [random.random()] * nx.number_of_nodes(g)  # random color...
        nx.draw(g,
                pos,
                node_size=40,
                node_color=c,
                vmin=0.0,
                vmax=1.0,
                with_labels=False)
    plt.show()
