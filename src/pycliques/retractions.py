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
suspc5 = list7[822]
suspc5 = list7[822]
g = list8[11045]
kg = pk(g)
k2g = pk(kg)
k2gl = nx.convert_node_labels_to_integers(k2g)
o4 = list8[11112]
retracts_to_suspc5 = list8[7901]
almost_retraction = {0: 0, 3: 2, 4: 3, 1: 1, 5: 4, 6: 5, 7: 6}
octa = nx.Graph()
octa.add_edges_from([("a", "b"), ("c", "d"), ("e", "f")])
octa = nx.complement(octa)
c4 = nx.cycle_graph(4)


def is_map(domain, codomain, ismap):
    for e in domain.edges():
        if e[0] in ismap and e[1] in ismap:
            w1 = ismap[e[0]]
            w2 = ismap[e[1]]
            if not(codomain.has_edge(w1, w2)) and w1 != w2:
                print("{} is an edge in domain".format(e))
                print("but {} {} is not an edge in codomain".format(w1, w2))
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
        print("w is now {}".format(w))
        common = common & closed_neighborhood(small, mapp[w])
        print("common is now {}".format(common))
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
            yield w
    else:
        for result in complete_retraction(large, small, ret):
            result[v] = w
            yield result


def ya_retraction(large, small, ret):
    remaining = list(large.nodes()-ret.keys())
    print("remaining={}", remaining)
    for v in remaining:
        for w in _extension_of_map(large, small, ret, v):
            print("Trying v={}, w={}".format(v, w))
            if len(ret) == len(large)-1:
                print("Hello! ret: {}. Yielding: {}".format(ret, (w,)))
                yield (w,)
            else:
                myret = copy.deepcopy(ret)
                myret[v] = w
                for result in ya_retraction(large, myret):
                    print("yielding {}".format((pos,)+result))
                    yield (pos,) + result


def yield_extend_retraction(large, small, ret):
    if len(ret) == len(large):
        print("Hello")
        yield ret
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


def conflict_retraction(large, small, ret, state, nextw):
    pass


def retraction_as_tuple(large, small, ret, state=()):
    remaining = tuple(large.nodes()-ret.keys())
    for pos in remaining:
        pass

    
def dict_to_tuple(the_dict):
    return tuple((a, b) for a, b in the_dict.items())


def invert_dict(the_dict):
    return dict((b, a) for a, b in the_dict.items())


def sa_retraction(large, small, state):
    ret = dict(state)
    remaining = list(large.nodes()-ret.keys())
    print("remaining = {}".format(remaining))
    for v in remaining:
        for w in _extension_of_map(large, small, ret, v):
            print("Trying v={}, w={}".format(v, w))
            if len(ret) == len(large)-1:
                print("Hello! ret: {}. Yielding: {}".format(ret, (v, w)))
                yield ((v, w),)
            else:
                for result in sa_retraction(large, small, state+((v, w),)):
                    print("yielding {}".format(((v, w),)+result))
                    yield ((v, w),)+result
