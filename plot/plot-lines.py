#!/usr/bin/python2.7

# Plots 
# usage: plot-lines x_col legend_col data_col title? comment? y_axis_title? maxy_range? miny_range?
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

def cmp_tags(a, b):
    try:
        return int (a) - int (b)
    except:
        l = ["Data", "Control", "Change_Owner", "Hints", "Requests&Replies", "Invalidations", "Replacements", 
             "0-hop", "2-hop", "3-hop", "+3-hop", "Persistent", "Mem",
             "Finding", "Waiting", "Solving",
             "FullMap-Inclusive", "FullMap", "CoarseVector (K=4)", "LimitedPointers (P=2)", "DupTag", "BinaryTree (SN=1)", "BinaryTree (SN=0)", "DASC (D=7)", "DASC (D=2)",
             "Hammer-CMP", "Hammer-Pointer", "Directory-CMP", "Token-CMP", "DiCo-CMP", "Hammer", "Directory", "DiCo-Base", "DiCo-Hints", "DiCo-Oracle", "DiCo-directory FS", "DiCo-FullMap FS", "DiCo-directory AS", "DiCo-FullMap AS", "DiCo-Pointer AS", "DiCo-snooping", "DiCo-snooping AS", "DiCo-NoSC AS",
             "DiCo-directory Base_64", "DiCo-directory Base_256", "DiCo-directory Base_1024", "DiCo-directory Base_4096",
             "DiCo-directory AS_64", "DiCo-directory AS_256", "DiCo-directory AS_1024", "DiCo-directory AS_4096",
             "DiCo-snooping Base_64", "DiCo-snooping Base_256", "DiCo-snooping Base_1024", "DiCo-snooping Base_4096",
             "DiCo-snooping AS_64", "DiCo-snooping AS_256", "DiCo-snooping AS_1024", "DiCo-snooping AS_4096",
             "DiCo-directory Base_6", "DiCo-directory Base_7", "DiCo-directory Base_8", "DiCo-directory Base_9", "DiCo-directory Base_10", "DiCo-directory Base_11", "DiCo-directory Base_12", "DiCo-directory Base_13", "DiCo-directory Base_14",
             "DiCo-directory AS_6", "DiCo-directory AS_7", "DiCo-directory AS_8", "DiCo-directory AS_9", "DiCo-directory AS_10", "DiCo-directory AS_11", "DiCo-directory AS_12", "DiCo-directory AS_13", "DiCo-directory AS_14",
             "HammerDupTagBase", "HammerDupTagMergeSh", "HammerDupTagMergeAll",
             "Block_FixedBit", "Block_FirstTouch", "Page_FixedBit", "Page_FirstTouch", "L2Bank_FixedBit", "L2Bank_FirstTouch",
             "DiCo-CV-2", "DiCo-CV-4", "DiCo-LP-1", "DiCo-NoSC",
             "RR", 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, "FT",
             "XS", "S", "M", "L", "XL"]
        try:
            ia = l.index(a)
            ib = l.index(b)
            return ia - ib
        except:
            return cmp (a, b)

def my_cmp(a, b):
    try:
        return int (a[0]) - int (b[0])
    except:
        l = ["RR", "FT", "XS", "S", "M", "L", "XL"]
        try:
            ia = l.index(a[0])
            ib = l.index(b[0])
            return ia - ib
        except:
            return cmp (a, b)

def sorted_list_uniq(l):
    l = [i for i in Set (l)]
    l.sort (cmp_tags)
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

miny_range = 0
if len(args) >= 8 and args[7] != "":
    miny_range = float(args[7])

maxy_range = None
if len(args) >= 7 and args[6] != "":
    maxy_range = float(args[6])

y_axis_title = None
#if len(args) >= 6:
#    y_axis_title = args[5]
#else:
y_axis_title = "Normalized execution time"

title = None
#if len(args) >= 4:
 #   title = args[3]

comment = None
#if len(args) >= 5:
 #   comment = args[4]

x_col = int(args[0])
legend_col = int(args[1])
data_col = int(args[2])

theme.get_options()
data = chart_data.read_csv(stdin)
theme.output_format = "pdf"
print data[x_col]
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

#y_grid_interval = 0.05
#y_grid_interval = 0.1
if maxy_range - miny_range > 4:
    y_grid_interval = 0.5
if maxy_range - miny_range > 2.5:
    y_grid_interval = 0.3
elif maxy_range - miny_range > 1.5:
    y_grid_interval = 0.2
y_grid_interval = 10.0 ** (round(log(maxy, 10)) - 1)

def fix_value(x):
    # removes useless decimals (x.0)
    try:
        if int(x) == float(x):
            return int(x)
    except:
        return x
    return x

def format_angle(v):
    a = str (v)
    return "/a60{}"+a

x_tags = [fix_value(f) for f in sorted_list_uniq([r[x_col] for r in data])]

legend_tags = [fix_value(f) for f in sorted_list_uniq([r[legend_col] for r in data])]

#area_size = (mm_to_pt(300), mm_to_pt(200))
area_size = (mm_to_pt(120), mm_to_pt(80))
#area_size = (mm_to_pt(90), mm_to_pt(40))
#area_size = (mm_to_pt(60), mm_to_pt(40))
legend_x = 110 # Legend right
#legend_x = 55 # Legend left
#legend_y = -5 # Legend extra up
legend_y = -2 # Legend up
#legend_y = 37 # Legend down
legend_loc = (area_size[0] - mm_to_pt(legend_x), area_size[1] - mm_to_pt(legend_y))
x_axis_title = "SB Size"
legend_rows = 4

tick_mark_array = (tick_mark.square, tick_mark.gray70dia, tick_mark.x, tick_mark.tri, tick_mark.dtri, tick_mark.gray70square, tick_mark.star, tick_mark.circle3, tick_mark.dia, tick_mark.gray70tri, tick_mark.plus)
line_style_array = (line_style.T(color=color.brown, width=0.8), line_style.T(color=color.gold, width=0.8), line_style.T(color=color.darkseagreen, width=0.8), line_style.T(color=color.dodgerblue4, width=0.8), line_style.T(color=color.saddlebrown, width=0.8), line_style.T(color=color.mediumvioletred, width=0.8), line_style.T(color=color.purple, width=0.8), line_style.T(color=color.darkgreen, width=0.8), line_style.T(color=color.red, width=0.8), line_style.T(color=color.gray30, width=0.8), line_style.T(color=color.blue, width=0.8))

#fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90

ar = area.T(size = area_size,
            x_coord = category_coord.T([[i] for i in x_tags], 0),
#            x_coord = linear_coord.T(),
#            x_range = (min(series), max(series)),
            #y_range = (miny_range, maxy_range),
            y_range = (0.3, 1.1),
            y_grid_interval = y_grid_interval,
            x_axis = axis.X(label=x_axis_title),#, tic_interval = 1, format="/a %s"),
            y_axis = axis.Y(label=y_axis_title),# format = "%.1f%%"),
            legend = nodupslegend.T(nr_rows = legend_rows, loc = legend_loc))

for legend_i in range(len(legend_tags)):
    x_data = [(r[x_col], r[data_col], r[data_col + 1]) for r in data if r[legend_col] == legend_tags[legend_i]]
    x_data.sort (my_cmp)
    ar.add_plot(line_plot.T(data = x_data,
                            tick_mark = tick_mark_array[legend_i%len(tick_mark_array)],
                            line_style = line_style_array[legend_i%len(line_style_array)],
                            label = str(legend_tags[legend_i]),
                            error_bar = error_bar.bar2, y_error_minus_col = 2))

ar.draw()

title_x = 5 #25
title_y = 0 #25
if title:
    title_text = "/hC/14{" + font.quotemeta(title) + "}"
    title_loc = ((area_size[0] - mm_to_pt(title_x)) / 2 - font.text_width(title_text) / 2, area_size[1] + mm_to_pt(title_y))
    tb = text_box.T(loc = title_loc, line_style = None, text = title_text)
    tb.draw()

if comment:
    comment_text = "{" + font.quotemeta(comment) + "}"
    comment_loc = (mm_to_pt(-8), mm_to_pt(-25))
    tb = text_box.T(loc = comment_loc, line_style = None, text = comment_text)
    tb.draw()

