import sys

from getjdeps import *
from packages import mpdg

from src.basicgraph import getcircles, show_pcircle

location = ""
for arg in sys.argv[1:]:
    if not arg.startswith("-"):
        location = arg
        break

cdg = get_jdependencies(location)
pdg, edges = mpdg(cdg)
for circle in getcircles(pdg):
    show_pcircle(circle)
