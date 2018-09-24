import re

from getjdeps import parse_jdeps
from packages import mpdg


def getacircle(graph: dict):
    def found(u):
        if not u in graph:
            return False
        if u in reached:
            if u in path:
                path.append(u)
                return True
            return False
        path.append(u)
        reached.add(u)
        for v in graph[u]:
            if found(v):
                return True
        path.pop()
        return False

    path = []
    reached = set()
    rest = set(graph)
    while len(rest) > 0:
        if found(rest.pop()):
            return path[path.index(path[-1]):-1]
        rest -= reached
    return None


inputfile = r"C:\Dev\Pacsinteg\pacsinteg.dep"
with open(inputfile, encoding="utf-8") as f:
    cdg = parse_jdeps(f.read())
pdg, edges = mpdg(cdg)
circle = getacircle(pdg)
print(circle)
n = len(circle)
for i in range(n):
    edge = circle[i], circle[(i+1)%n]
    print(edges[edge])


