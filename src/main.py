import re

from getjdeps import parse_jdeps


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


inputfile = r"..\res\jdeptest"
