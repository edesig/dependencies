from src.tools import idset


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


## TO DO:
# understand coroutines to make
# a real generator implementation
# Note: on infinite graphs this generator
# could never throw a component, if there is
# a topological order without first element
def stronglyconnectedcomponents(g):
    """This Generator implements Tarjan's Algorithm that
    returns a topological order of the strongly connected components"""
    reached = idset()
    processed = set()
    stack = []
    components = list()

    def f(node):
        nonlocal reached, stack, g, processed
        if node in reached:
            return reached.id(node)
        stack.append(node)
        reached.add(node)
        if node not in g:
            r = reached.id(node)
        else:
            r = min([f(successor) for successor in g[node] if successor not in processed]
                    + [reached.id(node)])
        if r >= reached.id(node):
            component = set()
            while True:
                x = stack.pop()
                component.add(x)
                if x == node:
                    components.append(component)
                    processed |= component
                    return r
        return r

    rest = set(g)
    while len(rest) > 0:
        f(rest.pop())
        rest -= reached
    yield from components
    return


def traversefrom(g, s):
    reached = set()

    def f(node):
        nonlocal g, reached
        if node in reached:
            return
        reached.add(node)
        for child in g[node]:
            yield from f(child)
        yield node

    for node in f(s):
        yield node
