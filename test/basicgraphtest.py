import unittest
from context import *
from src.basicgraph import *

G = {1: {2},
     2: {3},
     3: {4},
     4: {2}}

acyclic = {1: {2, 3},
           2: {4},
           3: {4, 5, 6}}

G2 = {
    1: {2},
    2: {3, 1},
    3: {1, 4, 5},
    4: {},
    5: {6},
    6: {3},
    7: {1, 8},
    8: {7}
}


class verystronglyconnectedcomponent(dict):
    def __init__(self, first=0, last=0):
        pass


def circlenormalform(c):
    s = c.index(min(c))
    n = len(c)
    return [c[(i + s) % n] for i in range(n)]


class TestBasicGraphUtils(unittest.TestCase):

    def test_getacircle(self):
        self.assertEqual(circlenormalform([4, 2, 3]), circlenormalform(getacircle(G)), "Fail")
        self.assertIsNone(getacircle(acyclic), "Found a circle in an acyclic graph")

    def test_stronglyconnectedcomponent(self):
        SCC = stronglyconnectedcomponents(G)
        self.assertSetEqual({2, 3, 4}, next(SCC))
        self.assertSetEqual({1}, next(SCC))

        for component in stronglyconnectedcomponents(acyclic):
            self.assertEqual(1, len(component))

        for component in stronglyconnectedcomponents(G2):
            print(component)
            self.assertIn(component, [{1, 2, 3, 5, 6}, {4}, {8, 7}])
