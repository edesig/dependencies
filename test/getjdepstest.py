import unittest
from getjdeps import *


class TestPatterns(unittest.TestCase):

    def test_jardep(self):
        t_module = r"jdepend"
        t_jar = r"C:\Program Files\Java\jdk1.8.0_152\jre\lib\rt.jar"
        t_jardep = rf"{t_module} -> {t_jar}"
        m = p_jardep.search(t_jardep)
        self.assertIsNotNone(m, "Test string does't match.")
        self.assertEqual(t_module, m["module"], "Module parsed wrongly")
        self.assertEqual(t_jar, m["jar"], "Module parsed wrongly")

    def test_class(self):
        t_class = r"jdepend.framework.AbstractParser"
        t_module = r"jdepend"
        t_line = rf"   {t_class} ({t_module})"
        m = p_class.search(t_line)
        self.assertIsNotNone(m, "Test string does't match.")
        self.assertEqual(t_class, m["class"], "Module parsed wrongly")
        self.assertEqual(t_module, m["module"], "Module parsed wrongly")


#
# r"      -> java.io.IOException"
