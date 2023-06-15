import unittest
from io import StringIO
from unittest.mock import patch

from context import *

from dependencies.basicgraph import *

G = {1: {2}, 2: {3}, 3: {4}, 4: {2}}

acyclic = {1: {2, 3}, 2: {4}, 3: {4, 5, 6}}

G2 = {1: {2}, 2: {3, 1}, 3: {1, 4, 5}, 4: {}, 5: {6}, 6: {3}, 7: {1, 8}, 8: {7}}


class verystronglyconnectedcomponent(dict):
    def __init__(self, first=0, last=0):
        pass


class TestGetacircle(unittest.TestCase):
    def test_with_a_graph_with_one_circle(self):
        self.assertEqual([2, 3, 4], getacircle(G), "Failed to find any circle")

    def test_with_a_graph_without_circle(self):
        self.assertIsNone(getacircle(acyclic), "Found a circle in an acyclic graph")


class TestGetcircles(unittest.TestCase):
    def test_with_a_graph_with_one_circle(self):
        self.assertSetEqual({(2, 3, 4)}, getcircles(G), "Failed to find any circle")

    def test_with_a_graph_without_circle(self):
        self.assertSetEqual(
            set(), getcircles(acyclic), "Found a circle in an acyclic graph"
        )

    def test_with_G2(self):
        self.assertEqual(
            {(1, 2), (1, 2, 3), (3, 5, 6), (7, 8)},
            getcircles(G2),
            "Failed to find all circles",
        )

    def test_with_empty(self):
        self.assertEqual(
            set(), getcircles({}), "Failed to get circles from empty graph"
        )


class TestStronglyconnectedcomponent(unittest.TestCase):
    def test_with_a_graph_with_a_circle_and_an_other_component(self):
        expected = {frozenset(component) for component in ({1}, {2, 3, 4})}
        actual = {frozenset(component) for component in stronglyconnectedcomponents(G)}

        self.assertSetEqual(expected, actual, "Failed to determine components")

    def test_with_an_acyclic_graph(self):
        expected = {frozenset((node,)) for node in range(1, 7)}
        actual = {
            frozenset(component) for component in stronglyconnectedcomponents(acyclic)
        }
        self.assertSetEqual(expected, actual, "Failed to determine components")

    def test_with_G2(self):
        expected = {
            frozenset(component) for component in ((1, 2, 3, 5, 6), (4,), (8, 7))
        }
        actual = {frozenset(component) for component in stronglyconnectedcomponents(G2)}
        self.assertSetEqual(expected, actual, "Failed to determine components")

    def test_with_empty_graph(self):
        self.assertSetEqual(
            frozenset(),
            frozenset(stronglyconnectedcomponents({})),
            "Failed to determine strongly connected components in an empty graph",
        )
