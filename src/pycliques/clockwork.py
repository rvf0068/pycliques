import networkx as nx


def core(segments, neig_segments):
    core = nx.Graph()
    core.add_nodes_from(range(sum(segments)))
    for seg in range(len(segments)):
        if seg < len(segments)-1:
            for i in range(segments[seg]):
                curr_vertex = sum(segments[:seg])+i
                start_next = sum(segments[:(seg+1)])
                for j in range(neig_segments[seg][i]):
                    core.add_edge(curr_vertex, start_next+j)
        else:
            for i in range(segments[seg]):
                curr_vertex = sum(segments[:seg])+i
                start_next = 0
                for j in range(neig_segments[seg][i]):
                    core.add_edge(curr_vertex, start_next+j)
                    print(curr_vertex, start_next+j)
                    
