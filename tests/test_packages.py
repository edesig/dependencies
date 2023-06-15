import unittest
from io import StringIO
from unittest.mock import patch

from context import *

from dependencies.packages import *


class TestPattern(unittest.TestCase):
    def test_p_classfullname(self):
        t_package = "com.ge.med.common.util"
        t_class = "CustomLogger"
        t_fullname = f"{t_package}.{t_class}"
        m = p_fullclassname.search(t_fullname)
        self.assertIsNotNone(m)
        self.assertEqual(t_package, m["packagename"], "Package name parsed wrongly")
        self.assertEqual(t_class, m["classname"], "Classname parsed wrongly")


class TestShowPcircle(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_a_simple_circle(self, stdout):
        circle = ["package_A", "package_B"]
        edges = {
            ("package_A", "package_B"): [("A1", "B2")],
            ("package_B", "package_A"): [("B1", "A2"), ("B3", "A1")],
        }
        show_pcircle(circle, edges)
        expected = (
            "package_A -> package_B\n"
            + "\tpackage_A->package_B\n"
            + "\t\tA1 -> B2\n"
            + "\tpackage_B->package_A\n"
            + "\t\tB1 -> A2\n"
            + "\t\tB3 -> A1\n"
        )
        self.assertEqual(expected, stdout.getvalue())
