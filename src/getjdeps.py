import re
from collections import defaultdict

p_jardep = re.compile(r"(?P<module>\w+)\s+->\s+(?P<jar>.+\S)")
r_class = r"^\s+(?P<class>\S+)\s+\((?P<module>\w+)\)?"
r_dependedclass = r"^\s+->\s+(?P<dclass>\S+)\s*(?P<dmodule>\w+)?$"
p_class = re.compile(r_class,re.MULTILINE)
p_dependedclass = re.compile(r_dependedclass, re.MULTILINE)
p_classblock = re.compile(rf"{r_class}[\r\n]*({r_dependedclass}[\r\n]*)*", re.MULTILINE)

input_file = r""  # TO DO : get it from parameter


def parse_jdeps(s):
    deps = defaultdict(lambda: set())
    for block in p_classblock.finditer(s):
        cl = block["class"]
        for dline in p_dependedclass.finditer(block[0]):
            dcl = dline["dclass"]
            deps[cl].add(dcl)
    return deps
