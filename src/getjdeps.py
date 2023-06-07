import re
from collections import defaultdict
import subprocess

p_jardep = re.compile(r"(?P<module>\w+)\s+->\s+(?P<jar>.+\S)")
r_class = r"^\s+(?P<class>\S+)\s+\((?P<module>\w+)\)?"
r_dependedclass = r"^\s+->\s+(?P<dclass>\S+)\s*(?P<dmodule>\w+)?$"
p_class = re.compile(r_class)
p_dependedclass = re.compile(r_dependedclass)
p_classblock = re.compile(rf"{r_class}[\r\n]*({r_dependedclass}[\r\n]*)*", re.MULTILINE)
p_line = re.compile("[^\n\r]+")


def parse_jdeps(s):
    deps = defaultdict(lambda: set())
    for line in p_line.finditer(s):
        cline = p_class.match(line[0])
        if cline:
            cl = cline["class"]
            continue
        dline = p_dependedclass.match(line[0])
        if dline:
            dcl = dline["dclass"]
            deps[cl].add(dcl)
    return dict(deps)


def get_jdependencies(location):
    prc_jdeps = subprocess.Popen(
        ["jdeps", "-verbose:class", "-filter:none", location],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, err = prc_jdeps.communicate()
    output = output.decode("utf-8")
    return parse_jdeps(f"{output}\n")
