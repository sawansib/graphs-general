#!/usr/bin/python

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
             "Barnes", "Cholesky", "FFT", "Ocean", "Radiosity", "Raytrace-opt", "Volrend", "Water-Nsq", "Tomcatv", "Unstructured", "FaceRec", "MPGdec", "MPGenc", "SpeechRec", "Blackscholes", "Canneal", "Swaptions", "Fluidanimate", "x264", "Apache", "SPEC-JBB"]
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
        l = ["Hammer", "Hammer-Pointer", "Directory", "Token", "DiCo", "DiCo-Base", "DiCo-Hints", "DiCo-Hints FS", "DiCo-Hints FSL2", "DiCo-directory FS", "DiCo-FM", "DiCo-CV-2", "DiCo-CV-4", "DiCo-LP-1", "DiCo-Tri", "DiCo-BT", "DiCo-NoSC", "DiCo-FM-Excl", "DiCo-Pointer", "DiCo-FullMap", "DiCo-FullMap FS", "DiCo-directory AS", "DiCo-FullMap AS", "DiCo-Hints AS", "DiCo-Oracle", "DiCo-OracleSt", "DiCo-Pointer AS", "DiCo-snooping", "DiCo-snooping AS", "DiCo-NoSC AS",
             "MOESI-Requester", "MOESI-Provider", "MESI-Requester", "MESI-Provider",
             "DiCo-directory Base_64", "DiCo-directory Base_256", "DiCo-directory Base_1024", "DiCo-directory Base_4096",
             "DiCo-directory AS_64", "DiCo-directory AS_256", "DiCo-directory AS_1024", "DiCo-directory AS_4096",
             "DiCo-snooping Base_64", "DiCo-snooping Base_256", "DiCo-snooping Base_1024", "DiCo-snooping Base_4096",
             "DiCo-snooping AS_64", "DiCo-snooping AS_256", "DiCo-snooping AS_1024", "DiCo-snooping AS_4096",
             "DiCo-directory Base_6", "DiCo-directory Base_7", "DiCo-directory Base_8", "DiCo-directory Base_9", "DiCo-directory Base_10", "DiCo-directory Base_11", "DiCo-directory Base_12", "DiCo-directory Base_13", "DiCo-directory Base_14",
             "DiCo-directory AS_6", "DiCo-directory AS_7", "DiCo-directory AS_8", "DiCo-directory AS_9", "DiCo-directory AS_10", "DiCo-directory AS_11", "DiCo-directory AS_12", "DiCo-directory AS_13", "DiCo-directory AS_14",
             "Unlimited-FullMap", "Unlimited-CV-4", "Unlimited-LP-2", "DupTag-Base", "DupTag-ImplicitSh", "DupTag-ImplicitAll",
             "HammerDupTagBase", "HammerDupTagMergeSh", "HammerDupTagMergeAll",
             "Block_FixedBit", "Block_FirstTouch", "Page_FixedBit", "Page_FirstTouch", "Page_FirstTouch_nohome", "Page_CachePressure", "Page_CachePressure_nohome", "Page_RoundRobin", "Page_DARR_1", "Page_DARR_2", "Page_DARR_4", "Page_DARR_8", "Page_DARR_16", "Page_DARR_20", "Page_DARR_32", "Page_DARR_64", "Page_DARR_64_nohome", "Page_DARR_64_scal", "Page_DARR_128", "Page_DARR_128_nohome", "Page_DARR_128_scal", "Page_DARR_256", "Page_DARR_512", "Page_DARR_1024", "Page_DARR_ft", "L2Bank_FixedBit", "L2Bank_FirstTouch",
             "LSB-1way", "LSB-2way", "Adaptive-1way", "Adaptive-Decay-1way", "Adaptive-Decay-Replacement-1way", 
             "MOESI", "MOESI-ISI", "MESI-ISI",
             "LSB", "LSB_1", "LSB_2", "LSB_4", "Xor", "Xor_1", "Adaptive-BruteForce", "Adaptive-BruteForce_1", "Adaptive-Random", "Adaptive-SatCounter", "Adaptive-SatCounter4", "Adaptive-SatCounter2", "Adaptive-SatCounter2C-1.10", "Adaptive-SatCounter2C-1.10_1", "Adaptive", "Adaptive-0.2", "Adaptive-0.3", "Adaptive-0.4", "Adaptive-0.5", "Adaptive-0.6", "Adaptive-0.7", "Adaptive-0.8", "Adaptive-0.9", "LSB-2",
#             "magny-cours_8", "extended-magny-cours_8", "extended-magny-cours-OXstate_8", "extended-magny-cours-OXSXstate_8", "extended-magny-cours-bitvector_8", "extended-magny-cours_16", "extended-magny-cours-OXstate_16", "extended-magny-cours-OXSXstate_16", "extended-magny-cours-bitvector_16", "extended-magny-cours_32", "extended-magny-cours-OXstate_32", "extended-magny-cours-OXSXstate_32", "extended-magny-cours-bitvector_32",
             "magny-cours_8_MC", "magny-cours_8_MC-Nests", "extended-magny-cours_8_FPGA", "extended-magny-cours-OXstate_8_FPGA", "extended-magny-cours-OXSXstate_8_FPGA", "extended-magny-cours-bitvector_8_FPGA", "extended-magny-cours_16_FPGA", "extended-magny-cours-OXstate_16_FPGA", "extended-magny-cours-OXSXstate_16_FPGA", "extended-magny-cours-bitvector_16_FPGA", "extended-magny-cours_32_FPGA", "extended-magny-cours-OXstate_32_FPGA", "extended-magny-cours-OXSXstate_32_FPGA", "extended-magny-cours-bitvector_32_FPGA",
             "magny-cours_8", "magny-cours-S1_8", "magny-cours-S1-usetimeout_8", 
             "extended-magny-cours_8", "extended-magny-cours-S1_8", "extended-magny-cours-S1-usetimeout_8",
             "extended-magny-cours-OXstate_8", "extended-magny-cours-S1-OXstate_8", "extended-magny-cours-S1-usetimeout-OXstate_8", 
             "extended-magny-cours-OXSXstate_8", "extended-magny-cours-S1-OXSXstate_8", "extended-magny-cours-S1-usetimeout-OXSXstate_8",
             "extended-magny-cours-bitvector_8", "extended-magny-cours-S1-bitvector_8", "extended-magny-cours-S1-usetimeout-bitvector_8",
             "extended-magny-cours_16", "extended-magny-cours-S1_16", "extended-magny-cours-S1-usetimeout_16", 
             "extended-magny-cours-OXstate_16", "extended-magny-cours-S1-OXstate_16", "extended-magny-cours-S1-usetimeout-OXstate_16",
             "extended-magny-cours-OXSXstate_16", "extended-magny-cours-S1-OXSXstate_16", "extended-magny-cours-S1-usetimeout-OXSXstate_16",
             "extended-magny-cours-bitvector_16", "extended-magny-cours-S1-bitvector_16", "extended-magny-cours-S1-usetimeout-bitvector_16",
             "extended-magny-cours_32", "extended-magny-cours-S1_32", "extended-magny-cours-S1-usetimeout_32",
             "extended-magny-cours-OXstate_32", "extended-magny-cours-S1-OXstate_32", "extended-magny-cours-S1-usetimeout-OXstate_32",
             "extended-magny-cours-OXSXstate_32", "extended-magny-cours-S1-OXSXstate_32", "extended-magny-cours-S1-usetimeout-OXSXstate_32",
             "extended-magny-cours-bitvector_32", "extended-magny-cours-S1-bitvector_32", "extended-magny-cours-S1-usetimeout-bitvector_32",
             "mc_8-dies", "emc_8-dies", "emc-OXSX_8-dies", "emc-bitvector_8-dies", 
             "emc_16-dies", "emc-OXSX_16-dies", "emc-bitvector_16-dies",
             "emc_32-dies", "emc-OXSX_32-dies", "emc-bitvector_32-dies",
             "Ideal", "OS"]
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

if maxy_range < 2:
    y_grid_interval = 0.1
elif maxy_range < 4:
    y_grid_interval = 0.2
elif maxy_range < 10:
    y_grid_interval = 0.5
elif maxy_range < 20:
    y_grid_interval = 1
elif maxy_range < 50:
    y_grid_interval = 2
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
apps.append("Average")

frame_x = 160
frame_y = 40
area_size = (mm_to_pt(frame_x), mm_to_pt(frame_y))
#legend_x = 110 #240 # 25 # Legend right
legend_x = frame_x - 3 # Legend left
#legend_y = -3 # -5 # Legend extra up
#legend_y = 15 # Legend up
legend_y = 38 # Legend down
legend_loc = (area_size[0] - mm_to_pt(legend_x), area_size[1] - mm_to_pt(legend_y))
x_axis_title = ""
width_bars = (float(frame_x) / 1.2) / float(len(series) * len(apps))
legend_rows = 4

tick_mark_array = (tick_mark.x, tick_mark.square, tick_mark.tri, tick_mark.star, tick_mark.dia, tick_mark.dtri, tick_mark.plus, tick_mark.x)
line_style_array = (None, line_style.T(color=color.blue, width=0.8), line_style.T(color=color.brown, width=0.8), line_style.T(color=color.gold, width=0.8), line_style.T(color=color.green4, width=0.8), line_style.T(color=color.purple, width=0.8))

#fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90

my_fill_style = (fill_style.gray20, fill_style.gray70, fill_style.diag, fill_style.gray50, fill_style.white, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)

my_fill_style_color = (fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90, fill_style.Plain(bgcolor=color.steelblue2), fill_style.Plain(bgcolor=color.mistyrose))

blas_fill_style_color = (fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

chronis_fill_style_color = (fill_style.Plain(bgcolor=color.brown), fill_style.Plain(bgcolor=color.goldenrod), fill_style.Plain(bgcolor=color.darkseagreen), fill_style.Plain(bgcolor=color.dodgerblue4), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.Plain(bgcolor=color.plum), fill_style.gray90)

ar = area.T(size = area_size,
            x_coord = category_coord.T([[i] for i in apps], 0),
            y_range = (miny_range, maxy_range),
            y_grid_interval = y_grid_interval,
            x_axis = axis.X(label = x_axis_title, format="/hR/a30%s", tic_label_offset=(0,0)),
            y_axis = axis.Y(label = y_axis_title),
            legend = nodupslegend.T(nr_rows = legend_rows, loc = legend_loc))

#for serie_i in range(len(series)):

serie_i = 0
serie_data = [(r[benchmark_col], r[data_col], r[data_col + 1]) for r in data if r[series_col] == series[serie_i]]
serie_data.append(("Average", average([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
ar.add_plot(bar_plot.T(data = serie_data,
#                       cluster = (serie_i, len(series)),
                       width = mm_to_pt(width_bars),
                       fill_style = blas_fill_style_color[serie_i%len(blas_fill_style_color)],
                       label = str(series[serie_i]),
                       error_bar = error_bar.bar2, error_minus_col = 2))
print >> stderr, series[serie_i], average([i[1] for i in serie_data])

serie_i = 1
serie_data = [(r[benchmark_col], r[data_col], r[data_col + 1]) for r in data if r[series_col] == series[serie_i]]
serie_data.append(("Average", average([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
ar.add_plot(line_plot.T(data = serie_data,
                        tick_mark = tick_mark_array[0],
                        line_style = line_style_array[0],
                        label = str(series[serie_i]),
                        error_bar = error_bar.bar2, y_error_minus_col = 2))
print >> stderr, series[serie_i], average([i[1] for i in serie_data])

print >> stderr, data

ar.draw()

# Average sep.
x = (ar.x_pos(apps[-1]) + ar.x_pos(apps[-2])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))

# Suite sep.
x = (ar.x_pos(apps[7]) + ar.x_pos(apps[8])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
x = (ar.x_pos(apps[9]) + ar.x_pos(apps[10])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
x = (ar.x_pos(apps[13]) + ar.x_pos(apps[14])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))
x = (ar.x_pos(apps[-3]) + ar.x_pos(apps[-4])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))

for serie_i in range(len(series)):
    for serie_j in range(len(apps)):
        value = [r[data_col] for r in data if r[series_col] == series[serie_i] and r[benchmark_col] == apps[serie_j]]
        if len(value) > 0:
            if value[0] > ar.y_range[1]:
                canvas.show(ar.x_pos(apps[serie_j]), ar.y_pos(ar.y_range[1]) - 7, "%.2f" % value[0])

title_x = -130 #80 #25
title_y = 4
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

