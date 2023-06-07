##Dependencies

## What is this?

This repo contains a lightweight tool to analize and resolve Java dependencies.

## How to use?

First compile your project, and run 
`python3 main.py [options] PROJECT_LOCATION``

options may be:
 -a, --scc to show class level strongly connected components
 At default this program shows the package level circles.
 
This toy gets the dependencies with "jdeps -verbose:class -filter:none", 
than it parses the output graph.

Only tested with jdeps 1.8.0_191.

## How to run unittests?

Unit tests can be executed from the project root with the command
`python -m unittest discover -p "*test.py" -s test/`
