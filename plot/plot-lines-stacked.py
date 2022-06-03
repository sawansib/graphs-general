#!/usr/bin/python2.7

# Plots 
# usage: plot-lines series_col stack_col benchmark_col data_col title? comment? y_axis_title? maxy_range? miny_range?
# input: csv data (error must be in data_col + 1)

from math import *
from sys import *
from sets import *
from pychart import *
import pychart.line_style
import pychart.canvas

import nodupslegend
import operator

def mm_to_pt(x):
    return x * 72 / 25.4

def duckcmp(a, b):
    try:
        return int (a) - int (b)
    except:
        l = ["Data", "Control", "Change_Owner", "Hints", "Requests&Replies", "Invalidations", "Replacements", 
             "0-hop", "2-hop", "3-hop", "+3-hop", "Persistent", "Mem",
             "Finding", "Waiting", "Solving"]
        try:
            ia = l.index(a)
            ib = l.index(b)
            return ia - ib
        except:
            return cmp (a, b)

def seriescmp(a, b):
    try:
        return int (a) - int (b)
    except:
        l = ["Token-CMP", "Hammer", "Hammer-Pointer", "Directory", "DiCo-Base", "DiCo-Hints", "DiCo-Oracle", "DiCo-directory FS", "DiCo-FullMap FS", "DiCo-directory AS", "DiCo-FullMap AS", "DiCo-Pointer AS", "DiCo-snooping", "DiCo-snooping AS", "DiCo-NoSC AS",
             "DiCo-directory Base_64", "DiCo-directory Base_256", "DiCo-directory Base_1024", "DiCo-directory Base_4096",
             "DiCo-directory AS_64", "DiCo-directory AS_256", "DiCo-directory AS_1024", "DiCo-directory AS_4096",
             "DiCo-snooping Base_64", "DiCo-snooping Base_256", "DiCo-snooping Base_1024", "DiCo-snooping Base_4096",
             "DiCo-snooping AS_64", "DiCo-snooping AS_256", "DiCo-snooping AS_1024", "DiCo-snooping AS_4096",
             "DiCo-directory Base_6", "DiCo-directory Base_7", "DiCo-directory Base_8", "DiCo-directory Base_9", "DiCo-directory Base_10", "DiCo-directory Base_11", "DiCo-directory Base_12", "DiCo-directory Base_13", "DiCo-directory Base_14",
             "DiCo-directory AS_6", "DiCo-directory AS_7", "DiCo-directory AS_8", "DiCo-directory AS_9", "DiCo-directory AS_10", "DiCo-directory AS_11", "DiCo-directory AS_12", "DiCo-directory AS_13", "DiCo-directory AS_14",
             "HammerDupTagBase", "HammerDupTagMergeSh", "HammerDupTagMergeAll",
             "Block_FixedBit", "Block_FirstTouch", "Page_FixedBit", "Page_FirstTouch", "L2Bank_FixedBit", "L2Bank_FirstTouch"]
        try:
            ia = l.index(a)
            ib = l.index(b)
            return ia - ib
        except:
            return cmp (a, b)

def sorted_list_uniq(l):
    l = [i for i in Set (l)]
    l.sort (duckcmp)
    return l

def sort_series(l):
    l = [i for i in l]
    l.sort (seriescmp)
    return l

def average(l):
    sum = 0.0
    for i in l:
        sum += i;
    return sum / len(l)

def average_error(l):
    sum = 0.0
    for i in l:
        sum += i * i;
    return sqrt(sum) / len(l)

args = theme.get_options()

if len(args) > 10:
    raise "Too many args"

series_group_size = 0
if len(args) >= 10 and args[9] != "":
    series_group_size = int(args[9])

miny_range = 0
if len(args) >= 9 and args[8] != "":
    miny_range = float(args[8])

maxy_range = None
if len(args) >= 8 and args[7] != "":
    maxy_range = float(args[7])

if len(args) >= 7:
    y_axis_title = args[6]
else:
    y_axis_title = "Normalized execution time"

title = None
if len(args) >= 5:
    title = args[4]

comment = None
if len(args) >= 6:
    comment = args[5]

series_col = int(args[0])
stack_col = int(args[1])
benchmark_col = int(args[2])
data_col = int(args[3])

theme.get_options()
data = chart_data.read_csv(stdin)
theme.output_format = "pdf"

maxy = 0
for r in data:
    maxy = max(maxy, r[data_col] + r[data_col + 1])

if maxy_range == None:
    max_ranges = []
    for j in range (0, int(ceil(log(maxy * 1.01, 10) + 1))):
        max_ranges = max_ranges + [i * 10 ** j for i in [1, 2, 5, 10, 25, 50, 75, 100, 150, 200, 500, 750, 1000]]
    max_ranges = [i for i in max_ranges if i > maxy * 1.001]
    max_ranges.sort ()
    maxy_range = max_ranges[0]

y_grid_interval = 10.0 ** (round(log(maxy, 10)) - 1)

def fix_serie(x):
    # removes useless decimals (x.0)
    try:
        if int(x) == float(x):
            return int(x)
    except:
        return x
    return x

series = [fix_serie(f) for f in sort_series(sorted_list_uniq([r[series_col] for r in data]))]
stackeds = [fix_serie(f) for f in sorted_list_uniq([r[stack_col] for r in data])]

realapps = sorted_list_uniq([r[benchmark_col] for r in data])
apps = [i for i in realapps]

area_size = (mm_to_pt(150), mm_to_pt(75))
#legend_x = 35 # Legend right
legend_x = 140 # Legend left
legend_y = -5 # Legend extra up
#legend_y = 15 # Legend up
#legend_y = 70 # Legend down
legend_loc = (area_size[0] - mm_to_pt(legend_x), area_size[1] - mm_to_pt(legend_y))
x_axis_title = ""
legend_rows = 6

tick_mark_array = (tick_mark.square, tick_mark.dia, tick_mark.star, tick_mark.tri, tick_mark.dtri, tick_mark.x, tick_mark.plus)

ar = area.T(size = area_size,
            x_coord = linear_coord.T(),
            x_range = (min(stackeds), max(stackeds)),
            y_range = (miny_range, maxy_range),
            y_grid_interval = y_grid_interval,
            x_axis = axis.X(label="/b"+x_axis_title, tic_interval=1),
            y_axis = axis.Y(label="/b"+y_axis_title, tic_interval=10),
            legend = nodupslegend.T(nr_rows = legend_rows, loc = legend_loc))

for app_i in range(len(apps)):
    app_data = [(r[stack_col], r[data_col], r[data_col + 1]) for r in data if r[benchmark_col] == apps[app_i]]
    line_data = sorted(app_data, key=operator.itemgetter(0))
    ar.add_plot(line_plot.T(data = line_data,
                            tick_mark = tick_mark_array[app_i%len(tick_mark_array)],
                            label = str(apps[app_i]),
                            error_bar = error_bar.bar2, y_error_minus_col = 2))

ar.draw()

title_x = -50 #25
if title:
    title_text = "/hC/14{" + font.quotemeta(title) + "}"
    title_loc = ((area_size[0] - mm_to_pt(title_x)) / 2 - font.text_width(title_text) / 2, area_size[1] + mm_to_pt(7))
    tb = text_box.T(loc = title_loc, line_style = None, text = title_text)
    tb.draw()

if comment:
    comment_text = "{" + font.quotemeta(comment) + "}"
    comment_loc = (mm_to_pt(-8), mm_to_pt(-25))
    tb = text_box.T(loc = comment_loc, line_style = None, text = comment_text)
    tb.draw()

