from networkx.algorithms import isomorphism
from pycliques.dominated import closed_neighborhood


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


def retraction2(large, small):
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    try:
        ret = next(rets)
        while len(ret) != len(large):
            exts = _extensions(large, small, ret)
            try:
                v, w = next(exts)
                ret[v] = w
            except StopIteration:
                return False
        return ret
    except StopIteration:
        return False


def retraction(large, small):
    GM = isomorphism.GraphMatcher(large, small)
    rets = GM.subgraph_isomorphisms_iter()
    while True:
        try:
            ret = next(rets)
            for v in large.nodes()-ret.keys():
                common = set(small.nodes())
                for w in large[v] & ret.keys():
                    common = common & closed_neighborhood(small, ret[w])
                    print("With v={}, w={}, the common set is {}".format(v, w, common))
                    for value in common:
                        print("Trying value={}".format(value))
                        ret[v] = value
                        print(len(ret), len(large))
                        if len(ret) == len(large):
                            return ret
                        else:
                            continue
        except StopIteration:
            break
