import unittest

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
