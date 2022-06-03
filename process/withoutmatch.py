#!/usr/bin/python2.7

# Finds the rows from a csv file that cannot be matched in another (no
# base case for normalization).
# Usage: withoutmatch.py data_file base_data_file first_data_column [matchcolumn]+
#     where: data_file and base_data_file are csv files with the same format, and
#            first_data_column is the column where the experiment value is stored,
#            and first_data_column + 1 is the column where the error is stored, and
#            matchcolumns will be used to select the line from base_data_file to
#            normalize each row of data_file.
#     output: csv data, with a row for each input row without a matching base case

import math
import sys
from pychart import chart_data

if len(sys.argv) < 5:
    raise "Wrong number of arguments"
datafn = sys.argv[1]
basefn = sys.argv[2]
fdc = int(sys.argv[3])
matchcols = [int(c) for c in sys.argv[4:]]

def lookup(t, matchcols, matchvalues):
    def filter_row(r):
        for (c, v) in zip(matchcols, matchvalues):
            if r[c] != v:
                return False
        return True
    return [r for r in t if filter_row(r)]

def lookup1(t, matchcols, matchvalues):
    l = lookup(t, matchcols, matchvalues)
    if len(l) == 1:
        return l[0]
    elif len(l) == 0: 
        return None # No base to normalize
    else:
        print l
        raise "Not unique key"

def divide_err(x, y):
    a = x[0]
    b = y[0]
    c = a / b
    ea = x[1]
    eb = x[1]
    ec = math.sqrt ((ea / a) ** 2 + (eb / b) ** 2) * c
    return (c, ec)

data = chart_data.read_csv(datafn)
base = chart_data.read_csv(basefn)
out = []
for row in data:
    baserow = lookup1(base, matchcols, [row[c] for c in matchcols])
    if baserow == None:
        out.append(row)
chart_data.write_csv(sys.stdout, out)
