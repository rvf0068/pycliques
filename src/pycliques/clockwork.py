"""Module for the construction of clockwork graphs."""

import itertools
import networkx as nx


def core(segments, neig_segments):
    """Returns the core graph with segments """
    core_graph = nx.Graph()
    core_graph.add_nodes_from(range(sum(segments)))
    segment_list = []
    for seg in range(len(segments)):
        segment_list.append(list(range(sum(segments[:seg]),
                                       sum(segments[:(seg+1)]))))
        for i in range(segments[seg]):
            curr_vertex = sum(segments[:seg])+i
            if seg < len(segments)-1:
                start_next = sum(segments[:(seg+1)])
            else:
                start_next = 0
            for j in range(neig_segments[seg][i]):
                core_graph.add_edge(curr_vertex, start_next+j)
    for segment in segment_list:
        pairs = itertools.combinations(segment, 2)
        core_graph.add_edges_from(pairs)
    return core_graph, segment_list


def crown(num_segments, size_segments, permutation):
    """Returns the crown graph with given segments and permutation"""
    crown_graph = nx.Graph()
    crown_graph.add_nodes_from(range(num_segments * size_segments))
    for seg in range(num_segments):
        for i in range(size_segments):
            curr_vertex = size_segments*seg + i
            if seg < num_segments-1:
                end_vertex = size_segments*(seg+1) + i
            else:
                end_vertex = permutation[i]
            crown_graph.add_edge(curr_vertex, end_vertex)
    segment_list = [list(range(size_segments*i, size_segments*(i+1)))
                    for i in range(num_segments)]
    for segment in segment_list:
        pairs = itertools.combinations(segment, 2)
        crown_graph.add_edges_from(pairs)
    return crown_graph, segment_list


def segmented_sum(segmented_b, segmented_c):
    """Returns the segmented sum of two segmented graphs"""
    graph_b = segmented_b[0]
    graph_c = segmented_c[0]
    segments_b = segmented_b[1]
    segments_c = segmented_c[1]
    segmented_sum_graph = nx.disjoint_union(graph_b, graph_c)
    new_segments_c = [[x+graph_b.order() for x in seg] for seg in segments_c]
    for seg in range(len(segments_c)):
        segmented_sum_graph.add_edges_from([(u, v) for u in segments_b[seg]
                                      for v in new_segments_c[seg]])
        if seg == len(segments_c)-1:
            next_seg = 0
        else:
            next_seg = seg+1
        segmented_sum_graph.add_edges_from([(u, v) for u in segments_b[next_seg]
                                      for v in new_segments_c[seg]])
    return segmented_sum_graph


def clockwork_graph(segments, neig_segments, size_seg_crown, permutation):
    """Returns the clockwork graph with given segments and data"""
    the_core = core(segments, neig_segments)
    the_crown = crown(len(segments), size_seg_crown, permutation)
    return segmented_sum(the_crown, the_core)

# for example, clockwork_graph([1,1,1], [[1], [0], [0]], 2, [1,0]) has
# iterated clique graphs with orders increasing by one
