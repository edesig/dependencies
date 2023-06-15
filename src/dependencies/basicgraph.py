from typing import Any, Dict, Generator, List, Optional, Set

from .tools import idset


def circlenormalform(c: List[Any]) -> List[Any]:
    # TODO: typing must reflect that Nodes are comparable
    # and the signature is List[T] -> List[T]
    """
    Gets the normal form of a circle that is a cycle starting with the least
    node.
    TODO: This normal form is not unique: See [1,2,3], [1, 3, 2]
    TODO: Do we need this?

    params:
    c: List of nodes representing a cycle
    """
    s = c.index(min(c))
    n = len(c)
    return [c[(i + s) % n] for i in range(n)]


def getacircle(graph: Dict[Any, Set[Any]]) -> Optional[List[Any]]:
    # UNUSED
    def found(u):
        nonlocal path, reached
        if not u in graph:
            return False
        if u in reached:
            if u in path:
                path.append(u)
                return True
            # return False
        path.append(u)
        reached.add(u)
        if any(found(v) for v in graph[u]):
            return True
        path.pop()
        return False

    path = []
    reached = set()
    rest = set(graph)
    while len(rest) > 0:
        if found(rest.pop()):
            return circlenormalform(path[path.index(path[-1]) : -1])
        rest -= reached
    return None


def getcircles(G: Dict[Any, Set[Any]]) -> Generator:
    """
    Generator getting all circles from a graph.

    params:
    G: the graph as an adjacency set of which circles we want to iterate
       through
    yields: circle as a list
    """
    reached = set()
    path = []
    circles = set()

    def f(w):
        nonlocal path, circles, reached
        if not w in G:
            # w has no edges out => w cannot be in a circle
            return
        path.append(w)  # step
        if path.count(w) > 1:
            # we've found a circle
            circles.add(tuple(circlenormalform(path[path.index(path[-1]) : -1])))
        else:
            reached.add(w)
            for v in G[w]:
                f(v)
        path.pop()  # step backward

    rest = set(G.keys())
    while rest:
        # path == []
        f(next(iter(rest)))
        # path == [] again
        rest -= reached
    return circles


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
            r = min(
                [f(successor) for successor in g[node] if successor not in processed]
                + [reached.id(node)]
            )
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
