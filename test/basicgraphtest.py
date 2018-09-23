import unittest
from context import getjdeps
from main import *

G = {1: {2},
     2: {3},
     3: {4},
     4: {2}}

acyclic = {1: {2, 3},
           2: {4},
           3: {4, 5, 6}}


def circlenormalform(c):
    s = c.index(min(c))
    n = len(c)
    return [c[(i + s) % n] for i in range(n)]


class TestBasicGraphUtils(unittest.TestCase):

    def test_getacircle(self):
        self.assertEqual(circlenormalform([4, 2, 3]), circlenormalform(getacircle(G)), "Fail")
        self.assertIsNone(getacircle(acyclic), "Found a tree in an acyclic graph")
