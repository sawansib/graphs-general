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
        l = ["Barnes", "Cholesky", "FFT", "FMM", "LU", "LU-nc", "Ocean", "Ocean-nc", "Radiosity", "Radix", "Raytrace", "Raytrace-opt", "Volrend", "Water-Nsq", "Water-Sp", 
             "FaceRec", "MPGdec", "MPGenc", "SpeechRec", 
             "Blackscholes", "Bodytrack", "Canneal", "Dedup", "Fluidanimate", "Streamcluster", "Swaptions", "Fluidanimate", "VIPS", "x264", 
             "Em3d", "Tomcatv", "Unstructured", 
             "Apache", "SPEC-JBB"]
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
        l = ["NoCoal", "All_NDRF", "Hybrid_DRF", "Hybrid_Manual", "Hybrid_Comp", "Hybrid_CompCI", "All_DRF", "NoFIFO", "TSO", "ROOW"]
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

if maxy_range - miny_range < 0.1:
    y_grid_interval = 0.01
elif maxy_range - miny_range < 0.2:
    y_grid_interval = 0.02
elif maxy_range - miny_range < 0.5:
    y_grid_interval = 0.05
elif maxy_range - miny_range < 2:
    y_grid_interval = 0.1
elif maxy_range - miny_range < 4:
    y_grid_interval = 0.2
elif maxy_range - miny_range < 8:
    y_grid_interval = 0.5
elif maxy_range - miny_range < 16:
    y_grid_interval = 1
elif maxy_range - miny_range < 50:
    y_grid_interval = 5
elif maxy_range - miny_range < 100:
    y_grid_interval = 5
elif maxy_range - miny_range < 200:
    y_grid_interval = 10
else:
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
#series = ['NoFusion', 'CISSR', 'FullFusion', 'IdealPF', 'PFNoSTinBW', 'PFNoNestedNCS', 'PFRepair']
#series = ['RISCVConsecutive', 'NCI+CISL+CINL']
#series = ['NoFusion','CICA', 'NCICA+NCISL+NCINL+CISL+CINL', 'RISCVall']
#series = ['TSO', 'ROOWR-7','ROOWR-12', 'ROOWR-13', 'ROOWR'] 
#series = ['NoFusion', 'Celio', 'Celio++', 'CISSR', 'IdealFusion', 'Predictor']
#series = ['RISCVFusion', 'CSF-SBR', 'RISCVFusion++','HELIOS', 'OracleFusion']
#series = ['NoFusion', 'HELIOS']
#series = ['CSF-SBR', 'RISCVFusion++', 'OracleFusion']


apps = sorted_list_uniq([r[benchmark_col] for r in data])
#apps = sorted_list_uniq('TSO')
apps.append("/bAverage")
#apps.append("/bGeomean")

if len(series) * len(apps) <= 20:
    frame_x = 120
elif len(series) * len(apps) <= 40:
    frame_x = 150
elif len(series) * len(apps) <= 60:
    frame_x = 120
elif len(series) * len(apps) <= 100:
    frame_x = 140
elif len(series) * len(apps) <= 200:
    frame_x = 200
else:
    frame_x = 400

frame_x = 100
maxy_range = 100
miny_range = 0
y_grid_interval = 20
frame_y = 25
area_size = (mm_to_pt(frame_x), mm_to_pt(frame_y))

if y_axis_title.find("%") >= 0:
    legend_rows = 1 #rows of legend
    legend_x = 5 * ceil(len(series)/legend_rows) + 56
    legend_y = -2
else:
    legend_rows = 1
    legend_x = frame_x - 189 #++ moves right -- moves left #250 #90 #Change legend position from here
    legend_y = -2           #++ down --up
if len(series) < 4:
    width_bars = (float(frame_x) / 1.5) / float(len(series) * len(apps)) 
else:
    width_bars = (float(frame_x) / 1.2) / float(len(series) * len(apps))

width_bars = 2
legend_loc = (area_size[0] - mm_to_pt(legend_x) - 20, area_size[1] - mm_to_pt(legend_y) - 1) #position of legend
x_axis_title = ""

def rgb(rx, gx, bx):
    return fill_style.Plain(bgcolor=color.T(r = rx / 256.0, g = gx / 256.0, b = bx / 256.0))

my_fill_style = [rgb(94,79,162),rgb(50,136,189),rgb(102,194,165),rgb(171,221,164),rgb(230,245,152),rgb(255,255,191),rgb(254,224,139),rgb(253,174,97),rgb(244,109,67),rgb(213,62,79),rgb(158,1,66)]

my_fill_style_len = len(my_fill_style)
my_line_style = [line_style.T(width = 1.5, color = my_fill_style[0 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[1 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[2 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[3 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[4 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[5 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[6 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[7 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[8 % my_fill_style_len].bgcolor, dash = None),
                 line_style.T(width = 1.5, color = my_fill_style[9 % my_fill_style_len].bgcolor, dash = None),
                 ]

my_line_style_len = len(my_line_style)

# my_fill_style = (fill_style.gray50, fill_style.gray90, fill_style.diag, fill_style.white, fill_style.gray20, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)

# my_fill_style_grouped = (fill_style.gray50, fill_style.gray70, fill_style.gray20, 
#                          fill_style.diag2, fill_style.Horiz(line_style=line_style.T(width=3), line_interval=6), fill_style.rdiag2, 
#                          fill_style.diag, fill_style.Horiz(line_style=line_style.T(width=0.4), line_interval=3), fill_style.rdiag, 
#                          fill_style.Diag(bgcolor=color.gray70, line_style=line_style.T(width=3), line_interval=6), fill_style.Horiz(bgcolor=color.gray70, line_style=line_style.T(width=3), line_interval=6), fill_style.Rdiag(bgcolor=color.gray70, line_style=line_style.T(width=3), line_interval=6), 
#                          fill_style.Diag(line_style=line_style.T(width=3, color=color.gray50), line_interval=6), fill_style.Horiz(line_style=line_style.T(width=3, color=color.gray50), line_interval=6), fill_style.Rdiag(line_style=line_style.T(width=3, color=color.gray50), line_interval=6))

# my_fill_style_color = (fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90, fill_style.Plain(bgcolor=color.steelblue2), fill_style.Plain(bgcolor=color.mistyrose))

#alexandra_fill_style_color = (fill_style.red, fill_style.gray30, fill_style.Plain(bgcolor=color.cornflowerblue), fill_style.red, fill_style.Rdiag(line_style=line_style.T(width=3, color=color.black), line_interval=6), fill_style.black, fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan))
#alexandra_fill_style_color = (fill_style.black, fill_style.gray30, fill_style.gray50, fill_style.Plain(bgcolor=color.darkseagreen),fill_style.Plain(bgcolor=color.cornflowerblue), fill_style.red, fill_style.Plain(bgcolor=color.tan))
#alexandra_fill_style_color = (fill_style.red, fill_style.gray30, fill_style.gray50, fill_style.Plain(bgcolor=color.darkseagreen),fill_style.Plain(bgcolor=color.cornflowerblue), fill_style.red, fill_style.Plain(bgcolor=color.tan))
alexandra_fill_style_color = (fill_style.Plain(bgcolor=color.cornflowerblue), fill_style.red, fill_style.gray30)

blas_fill_style_color = (fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

chronis_fill_style_color = (fill_style.Plain(bgcolor=color.dodgerblue4), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.Plain(bgcolor=color.plum), fill_style.gray90)

#chronis_fill_style_color = (fill_style.Plain(bgcolor=color.brown), fill_style.Plain(bgcolor=color.goldenrod), fill_style.Plain(bgcolor=color.darkseagreen), fill_style.Plain(bgcolor=color.dodgerblue4), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.Plain(bgcolor=color.plum), fill_style.gray90)

y_axis_title = "/hC/12{" + y_axis_title + "}"

if len(series) > 1:
    ar = area.T(size = area_size,
                x_coord = category_coord.T([[i] for i in apps], 0),
                y_range = (miny_range, maxy_range),
                y_grid_interval = y_grid_interval,
                x_axis = axis.X(label = x_axis_title , format="/hR/12/a60 %s"),
                y_axis = axis.Y(label = y_axis_title, label_offset = (0,0), format="/12/hR/a0 %s"), #(0,-10) changes the Y axis title position
                legend = nodupslegend.T(nr_rows = legend_rows, loc = legend_loc))
else:
    ar = area.T(size = area_size,
                x_coord = category_coord.T([[i] for i in apps], 0),
                y_range = (miny_range, maxy_range),
                y_grid_interval = y_grid_interval,
                x_axis = axis.X(label = x_axis_title, format="/hR/12/a60 %s"),
                y_axis = axis.Y(label = y_axis_title, label_offset = (0,0), format="/12/hR/a0 %s"),
                legend = None)

for serie_i in range(len(series)):
    serie_data = [(r[benchmark_col], r[data_col], r[data_col + 1]) for r in data if r[series_col] == series[serie_i]]
    serie_data.append(("/bAverage", average([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
    #serie_data.append(("/bGeomean", geomean([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
    ar.add_plot(bar_plot.T(data = serie_data,
                           cluster = (serie_i, len(series)),
                           width = mm_to_pt(width_bars),
                           fill_style = chronis_fill_style_color[serie_i%len(chronis_fill_style_color)],
                           #fill_style = my_line_style[serie_i%len(my_line_style)],
                           #fill_style = my_fill_style[serie_i%len(my_fill_style)],
                           #fill_style = alexandra_fill_style_color[serie_i%len(alexandra_fill_style_color)],
                           label = str(series[serie_i]),
                           error_bar = error_bar.bar2, error_minus_col = 2))
    print >> stderr, series[serie_i], average([i[1] for i in serie_data])
    #print >> stderr, series[serie_i], geomean([i[1] for i in serie_data])

print >> stderr, data

#add a normalization line at 1
#canvas.line(line_style.black, 0, ar.y_pos(1), mm_to_pt(frame_x), ar.y_pos(1))

ar.draw()

# Average sep.
x = (ar.x_pos(apps[-1]) + ar.x_pos(apps[-2])) / 2
canvas.line(line_style.black_dash1, x, ar.y_pos(miny_range), x, ar.y_pos(ar.y_range[1]))

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
                    canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) , ar.y_pos(ar.y_range[1]) + 1, "/12{%.2f}" % value[0])  
                elif serie_i == 1:
                    # Here is placed left
                    #canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) - 12, ar.y_pos(ar.y_range[1]) - 7, "/7{%.2f}" % value[0])
                    # Here is placed up left
                    canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) , ar.y_pos(ar.y_range[1]) + 1, "/12{%.2f}" % value[0])
                elif serie_i == 2:
                    # Here is placed right
                    #canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) + 10, ar.y_pos(ar.y_range[1]) - 7, "/7{%.2f}" % value[0])
                    # Here is placed up right
                    canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) , ar.y_pos(ar.y_range[1]) + 1, "/12{%.2f}" % value[0])
                else:
                    # Here is placed up
                    canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars), ar.y_pos(ar.y_range[1]) + 1, "/12{%.2f}" % value[0])
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
title_y = 10

if title:
    title_text = "/hC/12{" + font.quotemeta(title) + "}"
    title_loc = ((area_size[0] - mm_to_pt(title_x)) / 2 - font.text_width(title_text) / 2, area_size[1] + mm_to_pt(title_y))
    tb = text_box.T(loc = title_loc, line_style = None, text = title_text)
    tb.draw()

if comment:
    comment_text = "{" + font.quotemeta(comment) + "}"
    comment_loc = (mm_to_pt(-10), mm_to_pt(-25))
    tb = text_box.T(loc = comment_loc, line_style = None, text = comment_text)
    tb.draw()

