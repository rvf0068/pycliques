import gzip

from pycliques.lists import _dict_small


def extract_graphs(the_list, order, the_file):
    index = 0
    translation = {}
    with gzip.open(_dict_small[order], 'rt') as graph_file:
        with open(the_file, 'w') as extracted_graphs:
            for graph in graph_file:
                if index in the_list:
                    translation[index] = graph.strip()
                index = index+1
            extracted_graphs.write(str(translation))
