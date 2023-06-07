import sys

from getjdeps import *
from packages import mpdg

from basicgraph import getcircles, show_pcircle, stronglyconnectedcomponents


def usage():
    print(
        """ Usage: python3 main.py [options] PROJECT_LOCATION
        
        PROJECT_LOCATION can be a .jar file or a java target directory
        
        Options:
        -a, -scc finds the strongly connected components on class level
        -p shows circles on package level.
        Note: only jdeps 1.8.0_191 is tested now.
        """
    )


location = ""
mode = "circles"
for arg in sys.argv[1:]:
    if not arg.startswith("-"):
        location = arg
    else:
        if arg in {"--scc", "-a"}:
            mode = "scc"
        if arg in {"--help", "-h"}:
            usage()
            exit()

if location == "":
    print("There is no input project location", file=sys.stderr)
    usage()

cdg = get_jdependencies(location)
if len(cdg) == 0:
    print(
        "There is no class-level dependency in the project. (or jdeps is not compatible)"
    )

pdg, edges = mpdg(cdg)
found_count = 0
if mode == "scc":
    for component in stronglyconnectedcomponents(cdg):
        if len(component) > 1:
            for element in component:
                print(element)
                found_count += 1
            print(" " * 3 + "-" * 27)
    if found_count == 0:
        print(
            f"There is no strongly connected component on class level in the project (modulo the correctness of this implementation"
        )
else:
    for circle in getcircles(pdg):
        found_count += 1
        show_pcircle(circle, edges)
    if found_count == 0:
        print(
            f"There is no circle on package level in the project (modulo the correctness of this implementation"
        )
