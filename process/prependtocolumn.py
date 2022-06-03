#!/usr/bin/python2.7

# Prepends some text to columns in csv data
# Usage: prependtocolumn.py [column text]+
#     input: csv data
#     output: csv data, text prepended

import math
import sys
from pychart import chart_data

if (len(sys.argv) - 1) % 2 != 0:
    raise "Odd number of arguments"

preps=[]
for i in range(1, len(sys.argv), 2):
    preps.append((int(sys.argv[i]), sys.argv[i+1]))

def prepend(r):
    for i in preps:
        r[i[0]] = i[1] + str(r[i[0]])
    return r

data = chart_data.read_csv(sys.stdin)
data = [prepend(r) for r in data]
chart_data.write_csv(sys.stdout, data)
