import os
import unittest

from context import *

from dependencies.getjdeps import *


class TestPatterns(unittest.TestCase):
    # positive tests

    def test_jardep(self):
        t_module = r"jdepend"
        t_jar = r"C:\Program Files\Java\jdk1.8.0_152\jre\lib\rt.jar"
        t_jardep = rf"{t_module} -> {t_jar}"
        m = p_jardep.search(t_jardep)
        self.assertIsNotNone(m, "Test string does'nt match.")
        self.assertEqual(t_module, m["module"], "Module name parsed wrongly")
        self.assertEqual(t_jar, m["jar"], "Jar path parsed wrongly")

    def test_class(self):
        t_class = r"jdepend.framework.AbstractParser"
        t_module = r"jdepend"
        t_line = rf"   {t_class} ({t_module})"
        m = p_class.search(t_line)
        self.assertIsNotNone(m, "Test string does'nt match.")
        self.assertEqual(t_class, m["class"], "Class name parsed wrongly")
        self.assertEqual(t_module, m["module"], "Module name parsed wrongly")

    def test_dependedclass(self):
        t_class = r"java.io.IOException"
        t_line = rf"      -> {t_class}"
        m = p_dependedclass.search(t_line)
        self.assertIsNotNone(m, "Test string does'nt match.")
        self.assertEqual(t_class, m["dclass"], "Class name parsed wrongly")
        self.assertEqual(None, m["dmodule"], "Module name parsed wrongly")

    def test_classblock(self):
        t_class = r"jdepend.framework.AbstractParser"
        t_module = r"jdepend"
        t_hline = rf"   {t_class} ({t_module})"
        t_dclass = r"java.io.IOException"
        t_bline = rf"      -> {t_dclass}"
        t_block = "{}\r\n{}\n".format(t_hline, "\r\n".join([t_bline] * 4))
        m = p_classblock.search(t_block)
        self.assertIsNotNone(p_class.search(t_hline), "Header Line does'nt match.")
        self.assertIsNotNone(
            p_dependedclass.search(t_bline), "Body line does'nt match."
        )
        self.assertIsNotNone(m, "Test string doesn't match.")
        self.assertEqual(t_class, m["class"], "Class name parsed wrongly")
        self.assertEqual(t_module, m["module"], "Module name parsed wrongly")
        self.assertEqual(t_dclass, m["dclass"], "Class name parsed wrongly")
        self.assertEqual(None, m["dmodule"], "Module name parsed wrongly")

        # Test for more blocks.
        k = 4
        t_block = "\r\n".join([t_block] * k) + "\n"
        n = len(p_classblock.findall(t_block))
        self.assertLessEqual(k, n, "Not all blocks are detected.")
        self.assertGreaterEqual(k, n, "Too many blocks are detected.")

    def test_line(self):
        t_line = "line"
        t_text = f"{t_line}\r\n{t_line}\n{t_line}\n\n{t_line}"
        for m in p_line.finditer(t_text):
            self.assertEqual(t_line, m[0])


class TestDepsParser(unittest.TestCase):
    def test_parse_jdeps(self):
        expected = {
            "com.edesig.proof.Even": {"com.edesig.proof.Main", "java.lang.Object"},
            "com.edesig.proof.Foo": {
                "java.io.PrintStream",
                "java.lang.Object",
                "java.lang.String",
                "java.lang.System",
            },
            "com.edesig.proof.Main": {
                "com.edesig.proof.Even",
                "com.edesig.proof.Odd",
                "java.io.PrintStream",
                "java.lang.Integer",
                "java.lang.Object",
                "java.lang.String",
                "java.lang.System",
            },
            "com.edesig.proof.Odd": {"com.edesig.proof.Main", "java.lang.Object"},
        }
        with open(os.path.join("res", "jdepstest.dep"), encoding="utf-8") as f:
            s = f.read()
        self.maxDiff = None
        self.assertDictEqual(
            expected, dict(parse_jdeps(s)), "Dependency graph is not parsed correctly"
        )
