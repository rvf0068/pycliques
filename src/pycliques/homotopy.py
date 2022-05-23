import networkx as nx
from pycliques.retractions import has_induced


def gen_triangles(graph):
    """Generator of the triangles of a graph

    Parameters
    ----------
    graph : NetworkX graph

    """
    nodes = list(graph.nodes())
    for i in nodes:
        i_index = nodes.index(i)
        for j in graph[i]:
            j_index = nodes.index(j)
            if j_index > i_index:
                for k in graph[j]:
                    k_index = nodes.index(k)
                    if k in graph[i] and k_index > j_index:
                        yield i, j, k


def condition_triangle_jbcs(graph):
    """Criterion to determine if a graph is homotopically invariant

    This function checks if every triangle in the graph is contained in a
    unique clique, and if the graph does not have an induced an octahedral
    graph.

    Parameters
    ----------
    graph : NetworkX graph
        Returns

    Examples
    --------
    5

    """
    cliques = list(nx.find_cliques(graph))
    for triangle in gen_triangles(graph):
        cont_triangle = [q for q in cliques if set(triangle).issubset(set(q))]
        if len(cont_triangle) >= 2:
            return triangle, cont_triangle
    else:
        hasit = has_induced(graph, nx.octahedral_graph())
        if not hasit:
            return True
        else:
            return hasit
