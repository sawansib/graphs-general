#!/usr/bin/python2.7
# Plots 
# usage: plot-bars series_col benchmark_col data_col title? comment? y_axis_title? maxy_range? miny_range?
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
        l = ["Data", "Control", "Change_Owner", "Hints", "Requests&Replies", "Invalidations&Acks", "Replacements", 
             "0-hop", "2-hop", "3-hop", "+3-hop", "Persistent", "Mem",
             "Hit", "Finding", "Waiting", "Memory", "Solving",
             "Barnes", "Cholesky", "FFT", "FMM", "LU", "LU-nc", "Ocean", "Ocean-nc", "Radiosity", "Radix", "Raytrace", "Raytrace-opt", "Volrend", "Water-Nsq", "Water-Sp", "Em3d", "Tomcatv", "Unstructured", "FaceRec", "MPGdec", "MPGenc", "SpeechRec", "Blackscholes", "Bodytrack", "Canneal", "Dedup", "Fluidanimate", "Ferret", "Swaptions", "x264", "Apache", "SPEC-JBB",
#             "Blackscholes", "Swaptions", "FFT", "Radix", "LU", "LU-nc", "Canneal", "Streamcluster", "Ferret", "Water-Sp", "Ocean-nc", "Ocean", "Raytrace", "Raytrace*", "Volrend", "Volrend*", "Dedup", "Water-Nsq", "Bodytrack", "Cholesky*", "FMM", "FMM*", "FMM**", "Barnes", "Barnes*", "Barnes**", "Radiosity", "Radiosity*", "Radiosity**", "Fluidanimate", "Raytrace-opt", "Em3d", "Tomcatv", "Unstructured", "FaceRec", "MPGdec", "MPGenc", "SpeechRec", "x264", "Apache", "SPEC-JBB",
             "MOESI", "Hybrid"]
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
        l = ["Base_XS", "Base_S", "Base_M", "Base_L", "Base_XL",
             "OS_XS", "OS_S", "OS_M", "OS_L", "OS_XL", 
             "Polly_XS", "Polly_S", "Polly_M", "Polly_L", "Polly_XL", 
             "Base_4", "Base_8", "Base_16", "Base_32",
             "OS_4", "OS_8", "OS_16", "OS_32",
             "Polly_4", "Polly_8", "Polly_16", "Polly_32",
             "MOESI", "Hybrid",
             "MESI", "MESI-TSO", "MESI_2000", "BSI-BSD", "BSI-BSD-PS", "BSI-BSD-PS-CB", "FSI-FSD", "FSI-FSD-PS", "FSI-FSD-PS-CB",
             "VIPS-M", "VIPS-M_1000", "VIPS-M-ideal", "TSO-B", "TSO-NA", "TSO-CB", "TSO-CV_32", "TSO-CV_64", "TSO-CV_128", "TSO-CVO_32", "TSO-CVO_64", "TSO-CVO_128",
             "Static", "Racer", "Racer-Perfect", "Racer-Perfect-Word", "Racer-Perfect-Block", "Racer-Perfect-Line", "Racer-16KB", "Racer-8KB", "Racer-4KB",
             "Racer-Word", "Racer-Line", "Racer-Bulk", "Racer-FineGrainBulk",
             "Racer-Inv", "Racer-CheckRace", "Racer-CheckRace-Hint", "Racer-Hint",
             "Racer_1000", "Racer-Hint_1000", "Racer-Hint_2000", "Racer-Hint_10000",
             "SISD-single", "SISD-ll&ss", "SISD-DoI-single", "SISD-DoI-ll&ss"]
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

if len(args) > 8:
    raise "Too many args"

if len(args) >= 8 and args[7] != "":
    miny_range = float(args[7])
else:
    miny_range = 0

maxy_range = None
if len(args) >= 7 and args[6] != "":
    maxy_range = float(args[6])

if len(args) >= 6:
    y_axis_title = args[5]
else:
    y_axis_title = "Normalized execution time"

title = None
if len(args) >= 4:
    title = args[3]

comment = None
if len(args) >= 5:
    comment = args[4]

series_col = int(args[0])
benchmark_col = int(args[1])
data_col = int(args[2])

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

if maxy_range < 0.1:
    y_grid_interval = 0.01
elif maxy_range < 0.5:
    y_grid_interval = 0.05
elif maxy_range < 2:
    y_grid_interval = 0.1
elif maxy_range < 4:
    y_grid_interval = 0.2
elif maxy_range < 8:
    y_grid_interval = 0.5
elif maxy_range < 16:
    y_grid_interval = 1
elif maxy_range < 50:
    y_grid_interval = 2
elif maxy_range < 100:
    y_grid_interval = 5
elif maxy_range < 200:
    y_grid_interval = 10
else:
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
apps = sorted_list_uniq([r[benchmark_col] for r in data])
#apps.append("/bGeomean")
apps.append("/bAverage")

if len(series) * len(apps) <= 20:
    frame_x = 80
elif len(series) * len(apps) <= 40:
    frame_x = 160
elif len(series) * len(apps) <= 60:
    frame_x = 200
elif len(series) * len(apps) <= 100:
    frame_x = 260
else:
    frame_x = 260
#frame_x = 200
frame_y = 40
area_size = (mm_to_pt(frame_x), mm_to_pt(frame_y))
#legend_x = 40 + 10 * len(series)
legend_y = 2 # 8 # 30 #-5
legend_x = frame_x - 4 #250 #90
#legend_x = 256
#legend_y = 37
legend_loc = (area_size[0] - mm_to_pt(legend_x), area_size[1] - mm_to_pt(legend_y))
x_axis_title = ""
width_bars = (float(frame_x) / 1.5) / float(len(series) * len(apps))
if len(series) <= 3:
    legend_rows = 1
else:
    legend_rows = 1

my_fill_style = (fill_style.gray50, fill_style.gray90, fill_style.diag, fill_style.white, fill_style.gray20, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)

my_fill_style_color = (fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90, fill_style.Plain(bgcolor=color.steelblue2), fill_style.Plain(bgcolor=color.mistyrose))

blas_fill_style_color = (fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

chronis_fill_style_color = (fill_style.Plain(bgcolor=color.brown), fill_style.Plain(bgcolor=color.goldenrod), fill_style.Plain(bgcolor=color.darkseagreen), fill_style.Plain(bgcolor=color.dodgerblue4), fill_style.Plain(bgcolor=color.lightgoldenrod4), fill_style.Plain(bgcolor=color.tan), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.gray90)

if len(series) > 1:
    ar = area.T(size = area_size,
                x_coord = category_coord.T([[i] for i in apps], 0),
                y_range = (miny_range, maxy_range),
                y_grid_interval = y_grid_interval,
                x_axis = axis.X(label = x_axis_title, format="/hR/a20%s"),
                y_axis = axis.Y(label = y_axis_title, label_offset = (0,-10)),
                legend = nodupslegend.T(nr_rows = legend_rows, loc = legend_loc))
else:
    ar = area.T(size = area_size,
                x_coord = category_coord.T([[i] for i in apps], 0),
                y_range = (miny_range, maxy_range),
                y_grid_interval = y_grid_interval,
                x_axis = axis.X(label = x_axis_title, format="/hR/a20%s"),
                y_axis = axis.Y(label = y_axis_title, label_offset = (0,-10)),
                legend = None)

canvas.line(line_style.black, 0, ar.y_pos(1), mm_to_pt(frame_x), ar.y_pos(1))

for serie_i in range(len(series)):
    serie_data = [(r[benchmark_col], r[data_col], r[data_col + 1]) for r in data if r[series_col] == series[serie_i]]
    #serie_data.append(("/bGeomean", geomean([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
    serie_data.append(("/bAverage", average([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
    ar.add_plot(bar_plot.T(data = serie_data,
                           cluster = (serie_i, len(series)),
                           width = mm_to_pt(width_bars),
#                           fill_style = my_fill_style[serie_i%len(my_fill_style)],
                           fill_style = chronis_fill_style_color[serie_i%len(chronis_fill_style_color)],
#                           fill_style = blas_fill_style_color[serie_i%len(blas_fill_style_color)],
#                           fill_style = my_fill_style_color[serie_i%len(my_fill_style_color)],
                           label = str(series[serie_i]),
                           error_bar = error_bar.bar2, error_minus_col = 2))
    #print >> stderr, series[serie_i], geomean([i[1] for i in serie_data])
    print >> stderr, series[serie_i], average([i[1] for i in serie_data])

print >> stderr, data

ar.draw()

# Average sep.
x = (ar.x_pos(apps[-1]) + ar.x_pos(apps[-2])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
#x = (ar.x_pos(apps[-2]) + ar.x_pos(apps[-3])) / 2
#canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))

# Suite sep.
# x = (ar.x_pos(apps[7]) + ar.x_pos(apps[8])) / 2
# canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
# x = (ar.x_pos(apps[9]) + ar.x_pos(apps[10])) / 2
# canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
# x = (ar.x_pos(apps[13]) + ar.x_pos(apps[14])) / 2
# canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
# x = (ar.x_pos(apps[-3]) + ar.x_pos(apps[-4])) / 2
# canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))

for serie_i in range(len(series)):
    value_avg = 0
    for serie_j in range(len(apps)):
        value = [r[data_col] for r in data if r[series_col] == series[serie_i] and r[benchmark_col] == apps[serie_j]]
        if len(value) > 0:
            value_avg += value[0]
            if value[0] > ar.y_range[1]:
                if serie_i == 2 and serie_j == 17:
                    # Here is placed up right
                    canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) + 6, ar.y_pos(ar.y_range[1]) + 1, "/7{%.2f}" % value[0])  
                elif serie_i == 1:
                    # Here is placed left
                    #canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) - 12, ar.y_pos(ar.y_range[1]) - 7, "/7{%.2f}" % value[0])
                    # Here is placed up left
                    canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) - 9, ar.y_pos(ar.y_range[1]) + 1, "/7{%.2f}" % value[0])
                elif serie_i == 2:
                    # Here is placed right
                    #canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) + 10, ar.y_pos(ar.y_range[1]) - 7, "/7{%.2f}" % value[0])
                    # Here is placed up right
                    canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) + 6, ar.y_pos(ar.y_range[1]) + 1, "/7{%.2f}" % value[0])
                else:
                    # Here is placed up
                    canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars), ar.y_pos(ar.y_range[1]) + 1, "/7{%.2f}" % value[0])
                	# Here is placed right
                	#canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) + 12, ar.y_pos(ar.y_range[1]) - 7, "/7{%.2f}" % value)
                	# Here is placed up right
                	#canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) + 6, ar.y_pos(ar.y_range[1]) + 1, "/7{%.2f}" % value)
    avg = value_avg / len(apps)
    if avg > ar.y_range[1]:
        if serie_i == 0:
            canvas.show(ar.x_pos(apps[serie_j]) - 28, ar.y_pos(ar.y_range[1]) + 1, "%.2f" % avg)
        elif serie_i == 1:
            canvas.show(ar.x_pos(apps[serie_j]) + 12, ar.y_pos(ar.y_range[1]) + 1, "%.2f" % avg)
        elif serie_i == 2:
            canvas.show(ar.x_pos(apps[serie_j]) + 7, ar.y_pos(ar.y_range[1]) - 7, "%.2f" % avg)
        else:
            canvas.show(ar.x_pos(apps[serie_j]) + 8, ar.y_pos(ar.y_range[1]) + 1, "%.2f" % avg)


title_x = 10
title_y = 2
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

