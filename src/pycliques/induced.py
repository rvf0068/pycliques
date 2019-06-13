import networkx as nx
import itertools
from networkx.algorithms.operators.unary import complement


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
    complement_graph = complement(graph)
    aux_graph = nx.Graph()
    edges_complement = complement_graph.edges()
    aux_graph.add_nodes_from(edges_complement)
    edges_pairs = itertools.combinations(edges_complement, 2)
    edges_pairs = [(e1, e2) for (e1, e2) in edges_pairs if _adyacency_f(complement_graph, (e1, e2))]
    aux_graph.add_edges_from(edges_pairs)
    cliques_aux = nx.find_cliques(aux_graph)
    while True:
        try:
            edges_octa = next(cliques_aux)
            if len(edges_octa) >= 3:
                vertices_octa = []
                for edge in edges_octa:
                    vertices_octa.extend(edge)
                octa = graph.subgraph(vertices_octa)
                cliques_octa = nx.find_cliques(octa)
                while True:
                    try:
                        clique_octa = next(cliques_octa)
                        if _is_clique(graph, clique_octa):
                            print(octa.nodes, clique_octa)
                            return True
                    except StopIteration:
                        break
        except StopIteration:
            break
    return False
