from inspect import getmembers, isfunction
from itertools import chain
import json
import metabolomics
import statistics
import sys

modules = [
    metabolomics,
    statistics
]

tasks = list(chain.from_iterable([getmembers(module, isfunction) for module in modules]))

if len(sys.argv) == 1:
    print json.dumps([t[1](_mode='json') for t in tasks], indent=2)
else:
    taskName = sys.argv[1]
    found = False
    for t in tasks:
        if t[1](_mode='json')['container_args'][0] == taskName:
            t[1](_mode='cli', args=sys.argv[2:])
            found = True

    if not found:
        sys.stderr.write('Task "%s" not found.\n' % (taskName,))
