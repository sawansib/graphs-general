#!/usr/bin/python2.7

# Calculates the average of several configurations, removing the varying 
# parameter. It discards the error.
# Usage: average-reduction.py reduced_column data_column
#     input: csv data, where the reduced_column is the varying parameter 
#            to be reduced into the average and the second parameter is the
#            data column.
#     output: csv data, with a row for each non-matching input row, and the 
#             average in the next column.

import math
import sys
from pychart import chart_data

if len(sys.argv) != 3:
    raise "Wrong number of arguments"
reduced_column = int(sys.argv[1])
data_column = int(sys.argv[2])

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
stats = {}
num_stats = {}
for r in data:
    if str(r[0:reduced_column]) not in stats:
        stats[str(r[0:reduced_column])] = float(r[data_column])
        num_stats[str(r[0:reduced_column])] = 1
    else:
        stats[str(r[0:reduced_column])] = stats[str(r[0:reduced_column])] + float(r[data_column])
        num_stats[str(r[0:reduced_column])] = num_stats[str(r[0:reduced_column])] + 1

for s in stats:
    print s.strip("[]'") + "," + str(stats[s] / num_stats[s]) + ",0.0"
