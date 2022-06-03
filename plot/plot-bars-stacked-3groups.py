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
             "Cold-cap-conf", "Coherence", "Coverage", "Self-inv", "Private-write", 
             "Shared", "Private",
             "Directory", "MESI", "MOESI", "OS", "xDRF", "RC-SC_optimal", "RC-SC", "RC-SC_512", "RC-SC_256", "RC-SC_128", "RC-SC_64", "RC-SC_32", "RC-SC_16", "RC-SC_8", "RC-SC_4", "RC-SC_2", "RC-SC_1",
             "FFT", "Ocean", "Radix", "Unstructured", "Avg. 16", "Ocean4", "Ocean8", "Radix4", "Mix4", "Mix8", "Avg. 32",
             "2mm", "3mm", "adi", "atax", "bicg", "covariance", "doitgen", "dudcmp", "durbin", "dynprog", "fdtd", "fdtd-2d", "fdtd-apml", "floyd-warshall", "floyd", "gemm", "gemver", "gesummv", "jacobi-1d-imper", "jacobi-2d-imper", "jacobi", "lu", "mvt", "seidel", "symm", "syr2k", "syrk", "trisolv", "trmm", "/bAvg. Polybench",
             "backprop", "bfs", "btree", "hotspot", "lavaMD", "nw", "particlefilter", "pathfinder", "/bAvg. Rodinia",
             "352.nab", "358.botsalgn", "359.botsspar", "367.imagick", "372.smithwa", "376.kdtree", "/bAvg. SpecOMP"]
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
        l = ["Base_XS", "Base_S", "Base_M", "Base_L", "Base_XL",
             "OS_XS", "OS_S", "OS_M", "OS_L", "OS_XL", 
             "Polly_XS", "Polly_S", "Polly_M", "Polly_L", "Polly_XL", 
             "Base_4", "Base_8", "Base_16", "Base_32",
             "OS_4", "OS_8", "OS_16", "OS_32",
             "Polly_4", "Polly_8", "Polly_16", "Polly_32",
             "Shared", "Private",
             "Directory", "Directory_6", "Directory_5", "Directory_4", "Directory_3", "Directory_2", "Directory_1", 
             "MESI", "MOESI", "OS", "xDRF", 
             "RC-SC_optimal", "RC-SC", "RC-SC_512", "RC-SC_256", "RC-SC_128", "RC-SC_64", "RC-SC_32", "RC-SC_16", "RC-SC_8", "RC-SC_6", "RC-SC_5", "RC-SC_4", "RC-SC_3", "RC-SC_2", "RC-SC_1",
             "SISD-single", "SISD-ll&ss", "SISD-DoI-single", "SISD-DoI-ll&ss",
             "SISD-Fwd-LLCSpin", "SISD-Fwd-NoBackOff", "SISD-Fwd-ExpBackOff", "SISD-Fwd-Callback"]
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
    some_not_cero = 0;
    for i in l:
        if i != 0:
            prod = prod * i;
            some_not_cero = 1
    if some_not_cero == 0:
        return 0.0
    else:
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

maxy = maxy * 2 # FIXME

if maxy_range == None:
    max_ranges = []
    for j in range (0, int(ceil(log(maxy * 1.01, 10) + 1))):
        max_ranges = max_ranges + [i * 10 ** j for i in [1, 2, 5, 10, 25, 50, 75, 100, 150, 200, 500, 750, 1000]]
    max_ranges = [i for i in max_ranges if i > maxy * 1.001]
    max_ranges.sort ()
    maxy_range = max_ranges[0]

if maxy_range < 1.4:
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
apps_a = [i for i in realapps]
apps_a.append("/bAvg. Polybench")
apps_a.append("/bAvg. Rodinia")
apps_a.append("/bAvg. SpecOMP")
apps = sorted_list_uniq(apps_a)
# apps1 = ("2mm", "3mm", "adi", "atax", "bicg", "covariance", "doitgen", "dudcmp", "durbin", "dynprog", "fdtd-2d", "fdtd-apml", "floyd-warshall", "gemm", "gemver", "gesummv", "jacobi-1d-imper", "jacobi-2d-imper", "lu", "mvt", "seided", "symm", "syr2k", "syrk", "trisolv", "trmm")
# apps1 = ("2mm", "3mm", "adi", "atax", "bicg", "covariance", "doitgen", "dudcmp", "durbin", "dynprog", "fdtd", "floyd", "gemm", "gemver", "gesummv", "jacobi", "lu", "mvt", "seidel", "symm", "syr2k", "syrk", "trisolv")
apps1 = ("adi", "bicg", "covariance", "dynprog", "fdtd", "mvt", "seidel", "trmm")
apps2 = ("backprop", "bfs", "btree", "hotspot", "particlefilter", "pathfinder")
#apps3 = ("352.nab", "358.botsalgn", "359.botsspar", "367.imagick", "372.smithwa", "376.kdtree")
apps3 = ("352.nab", "358.botsalgn", "359.botsspar", "367.imagick")

if len(series) <= 3:
    frame_x = 140
elif len(series) <= 6:
    frame_x = 160
else:
    frame_x = 200

# frame_x = 180

if max(len(stackeds), len(series)) <= 3:
    legend_rows = 1
else:
    legend_rows = 2
if len(series) < 4:
    width_bars = (float(frame_x) / 1.5) / float(len(series) * len(apps))
else:
    width_bars = (float(frame_x) / 1.2) / float(len(series) * len(apps))
frame_y = 40
area_size = (mm_to_pt(frame_x), mm_to_pt(frame_y))
legend_x = 45 # Legend right
#legend_x = 140 # Legend left
legend_y = -10 #-5 # Legend extra up
#legend_y = 15 # Legend up
#legend_y = 70 # Legend down
legend_loc = (area_size[0] - mm_to_pt(legend_x), area_size[1] - mm_to_pt(legend_y))
x_axis_title = ""

my_fill_style = (fill_style.gray20, fill_style.gray70, fill_style.diag, fill_style.gray50, fill_style.white, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)

ar = area.T(size = area_size,
            x_coord = category_coord.T([[i] for i in apps], 0),
            y_range = (miny_range, maxy_range),
            y_grid_interval = y_grid_interval,
            x_axis = axis.X(label = x_axis_title, format="/a90 %s"),
            y_axis = axis.Y(label = y_axis_title),
            legend = nodupslegend.T(nr_rows = legend_rows, loc = legend_loc))

avg1_total = []
avg2_total = []
avg3_total = []
for serie_i in range(len(series)):
    avg1_total.append(0)
    avg2_total.append(0)
    avg3_total.append(0)

for serie_i in range(len(series)):
    avg1_total[serie_i] = 0
    avg2_total[serie_i] = 0
    avg3_total[serie_i] = 0
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
	    serie_data.append(("/bAvg. Polybench", average([i[1] for i in serie_data1]), average_error([i[2] for i in serie_data1])));
            serie_data2 = [f for f in serie_data if f[0] in apps2]
            serie_data.append(("/bAvg. Rodinia", average([i[1] for i in serie_data2]), average_error([i[2] for i in serie_data2])));
            serie_data3 = [f for f in serie_data if f[0] in apps3]
            serie_data.append(("/bAvg. SpecOMP", average([i[1] for i in serie_data3]), average_error([i[2] for i in serie_data3])));
            p = bar_plot.T(data = serie_data,
                           cluster = (serie_i, len(series)),
                           width = mm_to_pt(width_bars),
                           fill_style = my_fill_style[stack_j],
                           label = str(stackeds[stack_j]),
                           error_bar = error_bar.bar2, error_minus_col = 2,
                           stack_on = prev_plot)
            ar.add_plot(p)
            prev_plot = p
            avg1_total[serie_i] = avg1_total[serie_i] + average([i[1] for i in serie_data1])
            avg2_total[serie_i] = avg2_total[serie_i] + average([i[1] for i in serie_data2])
            avg3_total[serie_i] = avg3_total[serie_i] + average([i[1] for i in serie_data3])
            #print >> stderr, "(", series[serie_i], ", 1.0, ", average([i[1] for i in serie_data1]), ", ", average([i[1] for i in serie_data2]), ", ", average([i[1] for i in serie_data3]), "),"
    print >> stderr, "(", series[serie_i], ", 1.0, ", avg1_total[serie_i], ", ", avg2_total[serie_i], ", ", avg3_total[serie_i], "),"

ar.draw()
lines_more_down = 70
x = (ar.x_pos(apps[-1]) + ar.x_pos(apps[-2])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range) - lines_more_down, x, ar.y_pos(ar.y_range[1]))
x1 = (ar.x_pos(apps[len(apps1)-1]) + ar.x_pos(apps[len(apps1)])) / 2
canvas.line(line_style.black_dash1, x1, ar.y_pos(miny_range) - lines_more_down, x1, ar.y_pos(ar.y_range[1]))
sep1 = (ar.x_pos(apps[len(apps1)]) + ar.x_pos(apps[len(apps1)+1])) / 2
canvas.line(line_style.T(color=color.black, width=1.2), sep1, ar.y_pos(miny_range) - lines_more_down, sep1, ar.y_pos(ar.y_range[1])+15)
x2 = (ar.x_pos(apps[len(apps1)+len(apps2)]) + ar.x_pos(apps[len(apps1)+len(apps2)+1])) / 2
canvas.line(line_style.black_dash1, x2, ar.y_pos(miny_range) - lines_more_down, x2, ar.y_pos(ar.y_range[1]))
sep2 = (ar.x_pos(apps[len(apps1)+len(apps2)+1]) + ar.x_pos(apps[len(apps1)+len(apps2)+2])) / 2
canvas.line(line_style.T(color=color.black, width=1.2), sep2, ar.y_pos(miny_range) - lines_more_down, sep2, ar.y_pos(ar.y_range[1])+15)

#half_x = (ar.x_pos(apps[1]) - ar.x_pos(apps[0]))/2
#one_bar = mm_to_pt(width_bars);
#half_w = mm_to_pt(width_bars*len(series)/2)
#canvas.line(line_style.black, ar.x_pos(apps[0]) - half_x, ar.y_pos(1), ar.x_pos(apps[0]) - half_w, ar.y_pos(1))
#canvas.line(line_style.black, ar.x_pos(apps[0]) + half_w, ar.y_pos(1), ar.x_pos(apps[1]) - half_w, ar.y_pos(1))
#canvas.line(line_style.black, ar.x_pos(apps[1]) + half_w, ar.y_pos(1), ar.x_pos(apps[4]) - half_w, ar.y_pos(1))
#canvas.line(line_style.black, ar.x_pos(apps[4]) - half_w + one_bar, ar.y_pos(1), ar.x_pos(apps[5]) - half_w, ar.y_pos(1))
#canvas.line(line_style.black, ar.x_pos(apps[5]) + half_w, ar.y_pos(1), ar.x_pos(apps[7]) - half_w, ar.y_pos(1))
#canvas.line(line_style.black, ar.x_pos(apps[7]) - half_w + one_bar*2, ar.y_pos(1), ar.x_pos(apps[8]) - half_w, ar.y_pos(1))
#canvas.line(line_style.black, ar.x_pos(apps[8]) + half_w - one_bar, ar.y_pos(1), ar.x_pos(apps[9]) - half_w, ar.y_pos(1))
#canvas.line(line_style.black, ar.x_pos(apps[9]) + half_w, ar.y_pos(1), ar.x_pos(apps[10]) - half_w, ar.y_pos(1))
#canvas.line(line_style.black, ar.x_pos(apps[-1]) - half_w + one_bar*2, ar.y_pos(1), ar.x_pos(apps[-1]) + half_x, ar.y_pos(1))

title1_x = frame_x * ((len(apps1)+1) / ((len(apps1)+len(apps2)+len(apps3)+3) * 2.0))
title2_x = frame_x * ((len(apps2)+1) / ((len(apps1)+len(apps2)+len(apps3)+3.0) * 2.0))
title3_x = frame_x * ((len(apps3)+1) / ((len(apps1)+len(apps2)+len(apps3)+3.0) * 2.0))
title_y = 2
if title:
    title_text = "/hC/12{" + font.quotemeta("Polybench") + "}"
    title_loc = (mm_to_pt(title1_x-10), area_size[1] + mm_to_pt(title_y))
    tb = text_box.T(loc = title_loc, line_style = None, text = title_text)
    tb.draw()

    title_text = "/hC/12{" + font.quotemeta("Rodinia") + "}"
    title_loc = (mm_to_pt(title1_x*2+title2_x-10), area_size[1] + mm_to_pt(title_y))
    tb = text_box.T(loc = title_loc, line_style = None, text = title_text)
    tb.draw()

    title_text = "/hC/12{" + font.quotemeta("SpecOMP") + "}"
    title_loc = (mm_to_pt((title1_x+title2_x)*2+title3_x-10), area_size[1] + mm_to_pt(title_y))
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
    

