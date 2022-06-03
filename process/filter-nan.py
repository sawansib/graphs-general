#!/usr/bin/python2.7

# Filters csv data
# Usage: filter.py [column]+
#     input: csv data
#     output: csv data, only those rows where the specified columns dont have NaNs or infinites

import math
import sys
from pychart import chart_data


constraints=[]
for i in range(1, len(sys.argv)):
    constraints.append(int(sys.argv[i]))

def python_does_not_have_isnan(v):
    vs = str(v).lower()
    return vs == "nan" or vs == "inf" or vs == "-inf"

def filter_row(r):
    for col in constraints:
        if python_does_not_have_isnan(r[col]) == True:
            return False
    return True

data = chart_data.read_csv(sys.stdin)
data = [r for r in data if filter_row(r)]
chart_data.write_csv(sys.stdout, data)
