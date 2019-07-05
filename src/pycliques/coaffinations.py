import networkx as nx
from networkx.algorithms import isomorphism


def coaffinations(graph, k):
    distance = dict(nx.all_pairs_shortest_path_length(graph))
    GM = isomorphism.GraphMatcher(graph, graph)
    autos = GM.subgraph_isomorphisms_iter()
    for auto in autos:
        for v in graph:
            if distance[v][auto[v]] < k:
                break
        else:
            yield auto
