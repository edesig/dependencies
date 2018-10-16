import sys

from getjdeps import *
from packages import mpdg

from basicgraph import getcircles, show_pcircle, stronglyconnectedcomponents

location = ""
mode = "circles"
for arg in sys.argv[1:]:
    if not arg.startswith("-"):
        location = arg
    else:
        if arg in {"--scc", "-a"}:
            mode = "scc"

cdg = get_jdependencies(location)
pdg, edges = mpdg(cdg)
if mode == "scc":
    for component in stronglyconnectedcomponents(cdg):
        if len(component)>1:
            for element in component:
                print(element)
            print(" " * 3 + "-" * 27)
else:
    for circle in getcircles(pdg):
        show_pcircle(circle, edges)
