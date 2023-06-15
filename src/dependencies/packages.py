import re
from collections import defaultdict
from typing import Dict, Set

p_fullclassname = re.compile(r"((?P<packagename>\S+)\.)?(?P<classname>\S+)")


def mpdg(cdg: Dict[str, Set[str]]):
    """
    Makes package dependency graph

    params:
    cdg    : class dependency graph as an adjacency set
    returns: (pdg, edges), where
        pdg is a package dependency graph as an adjacency set
        edges is a dict where edges are mapped to the class dependencies
        representing the package dependency represented by the edge
    """
    edges = defaultdict(lambda: set())
    pdg = defaultdict(lambda: set())
    for cl in cdg:
        m = p_fullclassname.match(cl)
        package = m["packagename"]
        for dcl in cdg[cl]:
            dm = p_fullclassname.match(dcl)
            dpackage = dm["packagename"]
            if dpackage == package:
                continue
            pdg[package].add(dpackage)
            edges[(package, dpackage)].add((cl, dcl))
    return dict(pdg), dict(edges)


def show_pcircle(circle, edges):
    print(" -> ".join(circle))
    n = len(circle)
    for i in range(n):
        edge = circle[i], circle[(i + 1) % n]
        print(f"\t{edge[0]}->{edge[1]}")
        for realization in edges[edge]:
            print(f"\t\t{' -> '.join(realization)}")
