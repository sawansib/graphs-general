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
        l = ["Invalidations", "Cold-cap-conf", "Coherence", "Selective-flushing", "Write-through", "Downgrades",
             "Barnes", "Cholesky", "FFT", "FMM", "LU", "Ocean", "Radiosity", "Radix", "Raytrace", "Raytrace-opt", "Volrend", "Water-Nsq", "Water-Sp", "Em3d", "Tomcatv", "Unstructured", "FaceRec", "MPGdec", "MPGenc", "SpeechRec", "Blackscholes", "Canneal", "Swaptions", "Fluidanimate", "x264", "Apache", "SPEC-JBB"]
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
        l = ["Hammer", "Directory", "Write-through", "WB-Pr_WT-Sh", "VIPS", "Directory-less", "VSiPS", "VIPS-M", "WT-shared", "WT-shared-delayed", "WT-sync-delayed", "Write-back"]
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

maxy = maxy * 2 # FIXME

if maxy_range == None:
    max_ranges = []
    for j in range (0, int(ceil(log(maxy * 1.01, 10) + 1))):
        max_ranges = max_ranges + [i * 10 ** j for i in [1, 2, 5, 10, 25, 50, 75, 100, 150, 200, 500, 750, 1000]]
    max_ranges = [i for i in max_ranges if i > maxy * 1.001]
    max_ranges.sort ()
    maxy_range = max_ranges[0]

if maxy_range < 1.2:
    y_grid_interval = 0.1
elif maxy_range < 2.4:
    y_grid_interval = 0.2
elif maxy_range < 6.0:
    y_grid_interval = 0.5
else:
    y_grid_interval = 10.0 ** (round(log(maxy, 10)) - 1)
#y_grid_interval = 0.1
#y_grid_interval = 1

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
apps.append("Average")

if len(series) <= 3:
    frame_x = 120
elif len(series) <= 6:
    frame_x = 260
else:
    frame_x = 300
#frame_x = 260
if len(stackeds) <= 3:
    legend_rows = 2
else:
    legend_rows = 2
if len(series) < 4:
    width_bars = (float(frame_x) / 1.5) / float(len(series) * len(apps))
else:
    width_bars = (float(frame_x) / 1.2) / float(len(series) * len(apps))
frame_y = 40
area_size = (mm_to_pt(frame_x), mm_to_pt(frame_y))
legend_x = 40 + 10 * len(stackeds)
legend_x = 10 + 22 * ceil(len(stackeds)/legend_rows)
#legend_y = -3
legend_x = 116
legend_y = 37
legend_loc = (area_size[0] - mm_to_pt(legend_x), area_size[1] - mm_to_pt(legend_y))
x_axis_title = ""

my_fill_style = (fill_style.gray20, fill_style.gray70, fill_style.diag, fill_style.gray50, fill_style.white, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)

my_fill_style2 = (fill_style.gray30, fill_style.gray70, fill_style.diag, fill_style.white, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)

my_fill_style_color = (fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

blas_fill_style_color = (fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

chronis_fill_style_color = (fill_style.Plain(bgcolor=color.brown), fill_style.Plain(bgcolor=color.goldenrod), fill_style.Plain(bgcolor=color.darkseagreen), fill_style.Plain(bgcolor=color.dodgerblue4), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

ar = area.T(size = area_size,
            x_coord = category_coord.T([[i] for i in apps], 0),
            y_range = (miny_range, maxy_range),
            y_grid_interval = y_grid_interval,
            x_axis = axis.X(label = x_axis_title, format="/hR/a30%s"), #
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
            serie_data.append(("Average", average([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
            p = bar_plot.T(data = serie_data,
                           cluster = (serie_i, len(series)),
                           width = mm_to_pt(width_bars),
                           fill_style = my_fill_style2[stack_j],
                           label = str(stackeds[stack_j]),
                           error_bar = error_bar.bar2, error_minus_col = 2,
                           stack_on = prev_plot)
            ar.add_plot(p)
            prev_plot = p
            print >> stderr, series[serie_i], average([i[1] for i in serie_data])

ar.draw()

# Average sep.
x = (ar.x_pos(apps[-1]) + ar.x_pos(apps[-2])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))

# # Suite sep.
# x = (ar.x_pos(apps[7]) + ar.x_pos(apps[8])) / 2
# canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
# x = (ar.x_pos(apps[9]) + ar.x_pos(apps[10])) / 2
# canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
# x = (ar.x_pos(apps[13]) + ar.x_pos(apps[14])) / 2
# canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
# x = (ar.x_pos(apps[-3]) + ar.x_pos(apps[-4])) / 2
# canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))

norm_line = 0 # put 1 to show a wide line at y=1
if norm_line == 1:
    half_x = (ar.x_pos(apps[1]) - ar.x_pos(apps[0]))/2
    one_bar = mm_to_pt(width_bars);
    half_w = mm_to_pt(width_bars*len(series)/2)
    canvas.line(line_style.black, ar.x_pos(apps[0]) - half_x, ar.y_pos(1), ar.x_pos(apps[0]) - half_w, ar.y_pos(1))
    canvas.line(line_style.black, ar.x_pos(apps[0]) + half_w, ar.y_pos(1), ar.x_pos(apps[1]) - half_w, ar.y_pos(1))
    canvas.line(line_style.black, ar.x_pos(apps[1]) + half_w, ar.y_pos(1), ar.x_pos(apps[4]) - half_w, ar.y_pos(1))
    canvas.line(line_style.black, ar.x_pos(apps[4]) - half_w + one_bar, ar.y_pos(1), ar.x_pos(apps[5]) - half_w, ar.y_pos(1))
    canvas.line(line_style.black, ar.x_pos(apps[5]) + half_w, ar.y_pos(1), ar.x_pos(apps[7]) - half_w, ar.y_pos(1))
    canvas.line(line_style.black, ar.x_pos(apps[7]) - half_w + one_bar*2, ar.y_pos(1), ar.x_pos(apps[8]) - half_w, ar.y_pos(1))
    canvas.line(line_style.black, ar.x_pos(apps[8]) + half_w - one_bar, ar.y_pos(1), ar.x_pos(apps[9]) - half_w, ar.y_pos(1))
    canvas.line(line_style.black, ar.x_pos(apps[9]) + half_w, ar.y_pos(1), ar.x_pos(apps[10]) - half_w, ar.y_pos(1))
    canvas.line(line_style.black, ar.x_pos(apps[-1]) - half_w + one_bar*2, ar.y_pos(1), ar.x_pos(apps[-1]) + half_x, ar.y_pos(1))

for serie_i in range(len(series)):
    for serie_j in range(len(apps)):
        value = 0.0
        for serie_k in range(len(stackeds)):
            if len([r[data_col] for r in data if r[series_col] == series[serie_i] and r[benchmark_col] == apps[serie_j] and r[stack_col] == stackeds[serie_k]]) == 1:
                value = value + float([r[data_col] for r in data if r[series_col] == series[serie_i] and r[benchmark_col] == apps[serie_j] and r[stack_col] == stackeds[serie_k]][0])
        if value > ar.y_range[1]:
            if serie_i == 0:
                canvas.show(ar.x_pos(apps[serie_j]) - 22, ar.y_pos(ar.y_range[1]) + 1, "%.1f" % value)
            elif serie_i == 1:
                canvas.show(ar.x_pos(apps[serie_j]) + 10, ar.y_pos(ar.y_range[1]) - 7, "%.1f" % value)
            elif serie_i == 2:
                canvas.show(ar.x_pos(apps[serie_j]) - 12, ar.y_pos(ar.y_range[1]) + 1, "%.2f" % value)
            else:
                canvas.show(ar.x_pos(apps[serie_j]) + 6, ar.y_pos(ar.y_range[1]) + 1, "%.2f" % value)

title_x = -25 #25
title_y = 4 # 6
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

legend_y = 5

if len(series) > 1:
    if len(series) < 4:
        legend_rows = 2 # len(series)
    else:
        legend_rows = 2
    index = 0
    bars_pos = 0
    bars_text = ""
    for i in series:
        bars_text = bars_text + str(index+1) + ". " + i + "\n"
        index = index + 1
        if (index % legend_rows) == 0:
            tb_bars = text_box.T(loc=(bars_pos+10,area_size[1] - mm_to_pt(legend_y)), text=bars_text, line_style=line_style.gray70_dash1)
            tb_bars.draw()
            bars_pos = bars_pos + font.get_dimension(bars_text)[1] + 16
            bars_text = ""

    while (index % legend_rows) != 0:
        bars_text = bars_text + " \n"
        index = index + 1
    if bars_text != "":
        tb_bars = text_box.T(loc=(bars_pos,area_size[1] - mm_to_pt(legend_y)), text=bars_text, line_style=line_style.gray70_dash1)
        tb_bars.draw()
    

