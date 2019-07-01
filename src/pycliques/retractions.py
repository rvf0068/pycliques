from networkx.algorithms import isomorphism
from pycliques.dominated import closed_neighborhood


def is_map(domain, codomain, ismap):
    for e in domain.edges():
        if e[0] in ismap and e[1] in ismap:
            w1 = ismap[e[0]]
            w2 = ismap[e[1]]
            if not(codomain.has_edge(w1, w2)) and w1 != w2:
                return False
    else:
        return True


def _extension_of_map(large, small, mapp, v):
    common = set(small.nodes())
    for w in large[v] & mapp.keys():
        common = common & closed_neighborhood(small, mapp[w])
    return common


def _first_retraction(large, small):
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    ret = next(rets)
    return ret


def dict_to_tuple(the_dict):
    return tuple((a, b) for a, b in the_dict.items())


def invert_dict(the_dict):
    return dict((b, a) for a, b in the_dict.items())


def _extend_retraction(large, small, state):
    ret = dict(state)
    remaining = list(large.nodes()-ret.keys())
    for v in remaining:
        for w in _extension_of_map(large, small, ret, v):
            if len(ret) == len(large)-1:
                yield ((v, w),)
            else:
                for res in _extend_retraction(large, small, state+((v, w),)):
                    yield ((v, w),)+res


def retraction(large, small):
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    for ret in rets:
        state = dict_to_tuple(ret)
        extension = _extend_retraction(large, small, state)
        for ext in extension:
            yield (dict(state+ext), invert_dict(ret))


def retracts(large, small):
    try:
        rets = retraction(large, small)
        return next(rets)
    except StopIteration:
        return False
