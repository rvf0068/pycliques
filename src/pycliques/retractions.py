from networkx.algorithms import isomorphism
from pycliques.dominated import closed_neighborhood


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
