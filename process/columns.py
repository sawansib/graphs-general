#!/usr/bin/python2.7

# Filters csv columns
# Usage: columns.py [column]+
#     input: csv data
#     output: csv data, only those columns which are specified

import math
import sys
from pychart import chart_data

columns = [int(c) for c in sys.argv[1:]]

def select_cols(row):
    ret = []
    for i in columns:
        ret.append(row[i])
    return ret

data = chart_data.read_csv(sys.stdin)
ndata = [select_cols(r) for r in data]
chart_data.write_csv(sys.stdout, ndata)
