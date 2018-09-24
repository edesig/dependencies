import sys

from getjdeps import *
from packages import mpdg

def circlenormalform(c):
    s = c.index(min(c))
    n = len(c)
    return [c[(i + s) % n] for i in range(n)]

def getacircle(graph: dict):
    def found(u):
        if not u in graph:
            return False
        if u in reached:
            if u in path:
                path.append(u)
                return True
            # return False
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

def getcircles(G):
    reached = set()
    path = []
    circles = set()

    def f(w):
        nonlocal path
        if not w in G:
            return
        path.append(w)
        if path.count(w) > 1:
            circles.add(tuple(circlenormalform(path[path.index(path[-1]):-1])))
            path.pop()
            return
        else:
            reached.add(w)
            for v in G[w]:
                f(v)
        path.pop()

    rest = set(G.keys())
    while rest:
        f(next(iter(rest)))
        rest -= reached
    return circles

def show_pcircle(circle):
    global edges
    print(" -> ".join(circle))
    n = len(circle)
    for i in range(n):
        edge = circle[i], circle[(i + 1) % n]
        print(f"\t{edge[0]}->{edge[1]}")
        for realization in edges[edge]:
            print(f"\t\t{' -> '.join(realization)}")
location = ""
for arg in sys.argv[1:]:
    if not arg.startswith("-"):
        location = arg
        break

cdg = get_jdependencies(location)
pdg, edges = mpdg(cdg)
for circle in getcircles(pdg):
    show_pcircle(circle)


