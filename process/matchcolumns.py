#!/usr/bin/python2.7

# Filter csv data by matching columns 
# Usage: matchcolumns.py [column column]+
#     input: csv data
#     output: csv data, only those rows where the pairs iof columns have the same value

import math
import sys
from pychart import chart_data

if (len(sys.argv) - 1) % 2 != 0:
    raise "Odd number of arguments"

constraints=[]
for i in range(1, len(sys.argv), 2):
    constraints.append((int(sys.argv[i]), int(sys.argv[i+1])))

def equals_to_str(val, strval):
    return type(val)(strval) == val

def matchcolumns_row(r):
    for (cola, colb) in constraints:
        if r[cola] != r[colb]:
            return False
    return True

data = chart_data.read_csv(sys.stdin)
data = [r for r in data if matchcolumns_row(r)]
chart_data.write_csv(sys.stdout, data)
