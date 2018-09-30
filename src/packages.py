import re
from collections import defaultdict

import getjdeps

p_fullclassname = re.compile(r"((?P<packagename>\S+)\.)?(?P<classname>\S+)")


def mpdg(cdg: dict):
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
