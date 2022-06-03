#!/usr/bin/python2.7

# Filters csv data
# Usage: filter.py [column value]+
#     input: csv data
#     output: csv data, only those rows where the constraints hold

import math
import sys
from pychart import chart_data

if (len(sys.argv) - 1) % 2 != 0:
    raise "Odd number of arguments"

constraints=[]
for i in range(1, len(sys.argv), 2):
    constraints.append((int(sys.argv[i]), sys.argv[i+1]))

def equals_to_str(val, strval):
    try:
        return type(val)(strval) == val
    except:
        return False

def filter_row(r):
    for (col, value) in constraints:
        if equals_to_str(r[col], value) != True:
            return False
    return True

data = chart_data.read_csv(sys.stdin)
data = [r for r in data if filter_row(r)]
chart_data.write_csv(sys.stdout, data)
