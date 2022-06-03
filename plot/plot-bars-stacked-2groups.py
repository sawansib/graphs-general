#!/usr/bin/python2.7

# Plots 
# usage: plot-bars-stacked series_col stack_col benchmark_col data_col title? comment? y_axis_title? maxy_range? miny_range?
# input: csv data (error must be in data_col + 1)

from math import *
from sys import *
from sets import *
from pychart import *
import pychart.line_style
import pychart.canvas

import nodupslegend

def mm_to_pt(x):
    return x * 72 / 25.4

def duckcmp(a, b):
    try:
        return int (a) - int (b)
    except:
        l = ["Data", "Control", "Change_Owner", "Hints", "Requests&Replies", "Invalidations", "Replacements", 
             "0-hop", "2-hop", "3-hop", "+3-hop", "Persistent", "Mem",
             "Hit", "Finding", "Waiting", "Memory", "Solving",
             "FFT", "Ocean", "Radix", "Unstructured", "Avg. 16", "Ocean4", "Ocean8", "Radix4", "Mix4", "Mix8", "Avg. 32",
             "barnes", "cholesky", "fft", "fmm", "lu_cb", "lu_ncb", "ocean_cp", "ocean_ncp", "radiosity", "radix", "raytrace", "volrend", "water_nsquared", "water_spatial", "/bAvg. Splash", 
             "blackscholes", "bodytrack", "canneal", "dedup", "ferret", "fluidanimate", "freqmine", "streamcluster", "swaptions", "vips", "x264", "/bAvg. Parsec"
             ]
        try:
            ia = l.index(a)
            ib = l.index(b)
            return ia - ib
        except:
            print >> stderr, a
            print >> stderr, b
            return cmp (a, b)

def seriescmp(a, b):
    try:
        return int (a) - int (b)
    except:
        l = ["LineCoal", "BulkCoal", "NoFIFOCoal",
             "WordSB", "LineSB", "CoalSB_Performance", "CoalSB_Energy", "RCSB"]
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

def geomean(l):
    prod = 1.0
    for i in l:
        if i != 0:
            prod = prod * i;
    return prod ** (1.0 / float(len(l)))

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

y_grid_interval = 10.0 ** (round(log(maxy_range - miny_range, 10)) - 1)

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
apps_a = [i for i in realapps]
apps_a.append("/bAvg. Splash")
apps_a.append("/bAvg. Parsec")
apps = sorted_list_uniq(apps_a)
apps1 = ("barnes", "cholesky", "fft", "fmm", "lu_cb", "lu_ncb", "ocean_cp", "ocean_ncp", "radiosity", "radix", "raytrace", "volrend", "water_nsquared", "water_spatial")
apps2 = ("blackscholes", "bodytrack", "canneal", "dedup", "ferret", "fluidanimate", "freqmine", "streamcluster", "swaptions", "vips", "x264")

frame_x = 200
frame_y = 40
area_size = (mm_to_pt(frame_x), mm_to_pt(frame_y))
legend_x = 25 # Legend right
#legend_x = 140 # Legend left
legend_y = -10 #-5 # Legend extra up
#legend_y = 15 # Legend up
#legend_y = 70 # Legend down
legend_loc = (area_size[0] - mm_to_pt(legend_x), area_size[1] - mm_to_pt(legend_y))
x_axis_title = ""
if len(series) < 4:
    width_bars = (float(frame_x) / 1.5) / float(len(series) * len(apps))
else:
    width_bars = (float(frame_x) / 1.2) / float(len(series) * len(apps))
legend_rows = 1

my_fill_style = (fill_style.gray20, fill_style.gray70, fill_style.diag, fill_style.gray50, fill_style.white, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)

ar = area.T(size = area_size,
            x_coord = category_coord.T([[i] for i in apps], 0),
            y_range = (miny_range, maxy_range),
            y_grid_interval = y_grid_interval,
            x_axis = axis.X(label = x_axis_title, format="/a90%s"),
            y_axis = axis.Y(label = y_axis_title),
            legend = nodupslegend.T(nr_rows = legend_rows, loc = legend_loc))

for serie_i in range(len(series)):
    prev_plot = None
    bar_plot.fill_styles.reset()
    for stack_j in range(len(stackeds)):
        serie_data = [(r[benchmark_col], r[data_col], r[data_col + 1]) for r in data if r[series_col] == series[serie_i] and r[stack_col] == stackeds[stack_j]]
        curr_apps = ([i[0] for i in serie_data])
        missing_apps = [i for i in realapps if i not in curr_apps]
        if missing_apps:
            m = [(i, 0.0, 0.0) for i in missing_apps]
            serie_data = serie_data + m
            serie_data.sort()

        if len([i[1] for i in serie_data]) > 0:
	    serie_data1 = [f for f in serie_data if f[0] in apps1]
	    serie_data.append(("/bAvg. Splash", average([i[1] for i in serie_data1]), average_error([i[2] for i in serie_data1])));
	    serie_data2 = [f for f in serie_data if f[0] in apps2]
	    serie_data.append(("/bAvg. Parsec", average([i[1] for i in serie_data2]), average_error([i[2] for i in serie_data2])));
            p = bar_plot.T(data = serie_data,
                           cluster = (serie_i, len(series)),
                           width = mm_to_pt(width_bars),
                           fill_style = my_fill_style[stack_j],
                           label = str(stackeds[stack_j]),
                           error_bar = error_bar.bar2, error_minus_col = 2,
                           stack_on = prev_plot)
            ar.add_plot(p)
            prev_plot = p
            print >> stderr, average([i[1] for i in serie_data])

ar.draw()
lines_more_down = 70
x = (ar.x_pos(apps[-1]) + ar.x_pos(apps[-2])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range) - lines_more_down, x, ar.y_pos(ar.y_range[1]))
x1 = (ar.x_pos(apps[len(apps1)-1]) + ar.x_pos(apps[len(apps1)])) / 2
canvas.line(line_style.black_dash1, x1, ar.y_pos(miny_range) - lines_more_down, x1, ar.y_pos(ar.y_range[1]))
sep1 = (ar.x_pos(apps[len(apps1)]) + ar.x_pos(apps[len(apps1)+1])) / 2
canvas.line(line_style.T(color=color.black, width=1.2), sep1, ar.y_pos(miny_range) - lines_more_down, sep1, ar.y_pos(ar.y_range[1])+15)

title1_x = 160 #80 #25
title2_x = 60 #80 #25
title_y = 2
if title:
    title_text = "/hC/14{" + font.quotemeta("Splash") + "}"
    title_loc = (area_size[0] - mm_to_pt(title1_x), area_size[1] + mm_to_pt(title_y))
    tb = text_box.T(loc = title_loc, line_style = None, text = title_text)
    tb.draw()

    title_text = "/hC/14{" + font.quotemeta("Parsec") + "}"
    title_loc = (area_size[0] - mm_to_pt(title2_x), area_size[1] + mm_to_pt(title_y))
    tb = text_box.T(loc = title_loc, line_style = None, text = title_text)
    tb.draw()

if comment:
    comment_text = "{" + font.quotemeta(comment) + "}"
    comment_loc = (mm_to_pt(-8), mm_to_pt(-25))
    tb = text_box.T(loc = comment_loc, line_style = None, text = comment_text)
    tb.draw()

index = 0
bars_pos = 0
bars_text = ""
for i in series:
    bars_text = bars_text + str(index+1) + ". " + i + "\n"
    index = index + 1
    if (index % legend_rows) == 0:
        tb_bars = text_box.T(loc=(bars_pos,area_size[1] - mm_to_pt(legend_y)), text=bars_text, line_style=line_style.gray70_dash1)
        tb_bars.draw()
        bars_pos = bars_pos + font.get_dimension(bars_text)[1] + 16
        bars_text = ""

while (index % legend_rows) != 0:
    bars_text = bars_text + " \n"
    index = index + 1
if bars_text != "":
    tb_bars = text_box.T(loc=(bars_pos,area_size[1] - mm_to_pt(legend_y)), text=bars_text, line_style=line_style.gray70_dash1)
    tb_bars.draw()
    

