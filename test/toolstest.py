import unittest
from context import *
from src.tools import dynamicdict, idset


class TestDynamicDict(unittest.TestCase):
    def f(self, k, n):
        if k == n - 1:
            return {0}
        if k < n:
            return set(range(k, n))
        raise KeyError

    def test_fibonacci(self):
        Fibonacci = dynamicdict(
            lambda k: Fibonacci[k - 1] + Fibonacci[k - 2], {0: 0, 1: 1}
        )
        self.assertEqual(
            218922995834555169026, Fibonacci[99], "Fibonacci miscalculated"
        )
        return

    def test_ga(self):
        ga = lambda n: dynamicdict(lambda k: self.f(k, n))
        n = 3
        self.assertSetEqual({0, 1, 2}, ga(3)[0])
        self.assertSetEqual({1, 2}, ga(3)[1])
        self.assertSetEqual({0}, ga(3)[2])


class TestIdSet(unittest.TestCase):
    def test(self):
        s = idset(range(10))
        s.append(range(6, 19))
        for element in s:
            self.assertEqual(element, s.id(element), "Wrong id")
            self.assertEqual(
                s.id(element), s[element], ".id is not equals to .__getitem__"
            )
        s = idset()
        s.append(range(0, 10, 2))
        for element in s:
            self.assertEqual(
                element / 2,
                s.id(element),
                "Perhaps something with the default constructor",
            )
        self.assertTrue(2 in s, "Operator in doesn't works well.")
        self.assertFalse(3 in s, "Operator in doesn't works well.")
        self.assertSetEqual(
            set(range(1, 10, 2)), set(range(10)) - s, "set difference is not correct"
        )
