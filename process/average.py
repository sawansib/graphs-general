#!/usr/bin/python2.7

# Calculates the average and std deviation of a several samples.
# Usage: average.py first_data_column
#     input: csv data, where the first first_data_column columns are the
#            experiment key and the rest of columns are samples.
#     output: csv data, with a row for each input row, the same key columns
#             and two columns instead of the samples (the average and the std
#             deviation).

import math
import sys
from pychart import chart_data

if len(sys.argv) != 2:
    raise "Wrong number of arguments"
fdc = int(sys.argv[1])

def stddev_list(list, delta = 1.0):
    list = [i for i in list if i != '' and i != '\n']
    total = 0.0
    numelems = len(list)
    for item in list:
        total += item
    mean = float(total) / numelems
    variance = 0.0
    for item in list:
        variance += (mean - item) ** 2
    if numelems > 1:
        stddev = math.sqrt(variance / (numelems - 1)) # sample std deviation
    else:
        stddev = 0
    return (mean, stddev * delta)

data = chart_data.read_csv(sys.stdin)
data = [r[0:fdc] + list(stddev_list(r[fdc:])) for r in data]
chart_data.write_csv(sys.stdout, data)
