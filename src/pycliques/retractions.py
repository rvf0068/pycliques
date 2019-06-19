from networkx.algorithms import isomorphism
from pycliques.dominated import closed_neighborhood
import copy


import networkx as nx
from pycliques.small import list7, list8
from pycliques.cliques import clique_graph
from pycliques.dominated import completely_pared_graph
from pycliques.induced import induced_octahedra


def pk(graph):
    return completely_pared_graph(clique_graph(graph))


suspc5 = list7[822]
g = list8[11045]
kg = pk(g)
k2g = pk(kg)
k2gl = nx.convert_node_labels_to_integers(k2g)
o4 = list8[11112]
retracts_to_suspc5 = list8[7901]
almost_retraction = {0: 0, 3: 2, 4: 3, 1: 1, 5: 4, 6: 5, 7: 6}


def is_map(domain, codomain, ismap):
    for e in domain.edges():
        if not(codomain.has_edge(ismap[e[0]], ismap[e[1]])):
            return False
    else:
        return True


def _extensions(large, small, mapp):
    for v in large.nodes()-mapp.keys():
        common = set(small.nodes())
        for w in large[v] & mapp.keys():
            common = common & closed_neighborhood(small, mapp[w])
        for value in common:
            yield (v, value)


def retraction(large, small):
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    try:
        ret = next(rets)
        while len(ret) != len(large):
            print("ret is now {}. len large={}, len ret={}".format(ret, len(large), len(ret)))
            exts = _extensions(large, small, ret)
            print("Possible extensions are {}".format(list(exts)))
            try:
                v, w = next(exts)
                ret[v] = w
            except StopIteration:
                return False
        return ret
    except StopIteration:
        return False


def _extension_of_map(large, small, mapp, v):
    common = set(small.nodes())
    for w in large[v] & mapp.keys():
        common = common & closed_neighborhood(small, mapp[w])
    return common


def extend_retraction(large, small, ret):
    therets = []
    if len(ret) == len(large):
        print("Hello")
        therets.append(ret)
    else:
        v = list(large.nodes()-ret.keys())[0]
        print("Finding image of vertex {}".format(v))
        possible = _extension_of_map(large, small, ret, v)
        print("Possible images are {}".format(possible))
        for w in possible:
            ret2 = copy.deepcopy(ret)
            ret2[v] = w
            print("Map is now {}".format(ret2))
            extend_retraction(large, small, ret2)
            print("len large={}, len ret={}".format(len(large), len(ret2)))
    return therets


def first_retraction(large, small):
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    ret = next(rets)
    return ret


def retraction3(large, small):
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    try:
        ret = next(rets)
        while len(ret) != len(large):
            print("ret is now {}. len large={}, len ret={}".format(ret, len(large), len(ret)))
            exts = _extensions(large, small, ret)
            for v, w in exts:
                ret[v] = w
            else:
                return False
        return ret
    except StopIteration:
        return False


def retraction_with_for(large, small):
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    try:
        ret = next(rets)
        remaining = list(large.nodes()-ret.keys())
        print("Remaining: {}".format(remaining))
        for v in remaining:
            possible = _extension_of_map(large, small, ret, v)
            print("v: {}, possible: {}".format(v, possible))
            if len(possible) == 0:
                return False
            else:
                for w in possible:
                    ret[v] = w
                    print("v: {}, remaining: {}".format(v, remaining))
                    remaining.remove(v)
        return ret
    except StopIteration:
        return False


def extension_almost_done(large, small, ret):
    remaining = list(large.nodes()-ret.keys())
    if len(remaining) == 1:
        v = remaining[0]
        for w in _extension_of_map(large, small, ret, v):
            ret[v] = w
            print("w={}".format(w))
            yield copy.deepcopy(ret)


def complete_retraction(large, small, ret):
    remaining = list(large.nodes()-ret.keys())
    v = remaining[0]
    if len(remaining) == 1:
        for w in _extension_of_map(large, small, ret, v):
            print("w={}".format(w))
            yield (w,)
    else:
        for result in _extension_of_map(large, small, ret, v):
            ret[v] = w
            complete_retraction(large, small,copy.deepcopy(ret))

