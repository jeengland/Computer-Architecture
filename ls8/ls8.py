#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

toRun = None

if len(sys.argv) > 1:
    toRun = sys.argv[1]
else:
    raise Exception('No program specified')

cpu.load(toRun)
cpu.run()
