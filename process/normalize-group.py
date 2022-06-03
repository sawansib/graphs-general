#!/usr/bin/python2.7

# Normalizes the results of some experiments with respect to some base experiments
# Usage: normalize-group.py data_file base_data_file first_data_column ignored_arg [matchcolumn]+
#     where: data_file and base_data_file are csv files with the same format, and
#            first_data_column is the column where the experiment value is stored,
#            and first_data_column + 1 is the column where the error is stored, and
#            matchcolumns will be used to select the line from base_data_file to
#            normalize each row of data_file. ignored_arg is ignored.
#     output: csv data, with a row for each input row, all columns unchanged except
#            first_data_column and first_data_column + 1, where the normalized value
#            and its error will be stored.

import math
import sys
from pychart import chart_data

if len(sys.argv) < 6:
    raise "Wrong number of arguments"
datafn = sys.argv[1]
basefn = sys.argv[2]
fdc = int(sys.argv[3])
matchcols = [int(c) for c in sys.argv[5:]]

def lookup(t, matchcols, matchvalues):
    def filter_row(r):
        for (c, v) in zip(matchcols, matchvalues):
            if r[c] != v:
                return False
        return True
    return [r for r in t if filter_row(r)]

def all_equal (l):
    for i in l[1:]:
        if i != l[0]:
            return False
    return True

def lookup1(t, matchcols, matchvalues):
    l = lookup(t, matchcols, matchvalues)
    if len(l) == 1:
        return l[0]
    elif len(l) == 0: 
        return None # No base to normalize
    else:
        if not all_equal (l):
            print >> sys.stderr, l
            raise "Not unique key"

def divide_err(x, y):
    a = x[0]
    b = y[0]
    if b == 0:
        if a == 0:
            return (float("nan"), 0)
        else:
            return (float("inf"), 0)
    c = a / b
    ea = x[1]
    eb = y[1]
    if a == 0:
        if ea == 0:
            ea_rel = 0
        else:
            ea_rel = float("inf")
    else:
        ea_rel = (ea / a)
    ec = math.sqrt (ea_rel ** 2 + (eb / b) ** 2) * c
    return (c, ec)

data = chart_data.read_csv(datafn)
base = chart_data.read_csv(basefn)
norm = []
for row in data:
    baserows = lookup(base, matchcols, [row[c] for c in matchcols])   
    if baserows != None:
        basevalue = (0, 0)
        for br in baserows:
            basevalue = (basevalue[0] + br[fdc], max(basevalue[1], br[fdc+1]))
        row = row[0:fdc] + list(divide_err(row[fdc:fdc + 2], basevalue)) + row[fdc + 2:]
        norm.append(row)
chart_data.write_csv(sys.stdout, norm)
