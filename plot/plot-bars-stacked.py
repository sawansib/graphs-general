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
        l = ["Replacements", "Invalidations", "Cold", "Capacity", "Conflict", "Cold-cap-conf", "Coherence", "Selective-flushing", "Write-through", "Downgrades", "Self-inv",
             "Barnes", "Cholesky", "FFT", "FMM", "LU", "LU-nc", "Ocean", "Ocean-nc", "Radiosity", "Radix", "Raytrace", "Raytrace-opt", "Volrend", "Water-Nsq", "Water-Sp", 
             "FaceRec", "MPGdec", "MPGenc", "SpeechRec", 
             "Blackscholes", "Bodytrack", "Canneal", "Dedup", "Fluidanimate", "Streamcluster", "Swaptions", "Fluidanimate", "VIPS", "x264", 
             "Em3d", "Tomcatv", "Unstructured", 
             "Apache", "SPEC-JBB",
             "Mix4", "Mix8", "Ocean4", "Radix4", "Ocean8", "Radix8",
             "L1", "LLC", "Network", "TLB", "R-Tag",
             "Shared", "Private", 
             "Read-write", "Read-only",
             "MOESI", "Directory", "Hybrid", "Hybrid-512", "Hybrid-4",
             "RoB", "LQ", "SQ", "SB", "SQ-SB",
             "L1_Tag", "L1_Read", "L1_Write", "SQSB_Search", "SQSB_Read", "SQSB_Write",
             "SQSB-Full", "SB-NotEmpty",
             "TSO_56", "ROOW_56", "ROOW_52", "ROOW_48", "ROOW_44", "ROOW_40", "ROOW_36", "ROOW_32", "ROOW_28", "ROOW_24", "ROOW_20", "ROOW_16"]
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
        l = ["NoCoal", "All_NDRF", "Hybrid_DRF", "Hybrid_Manual", "Hybrid_Comp", "Hybrid_CompCI", "All_DRF", "NoFIFO",
             "TSO_56", "ROOW_56", "ROOW_52", "ROOW_48", "ROOW_44", "ROOW_40", "ROOW_36", "ROOW_32", "ROOW_28", "ROOW_24", "ROOW_20", "ROOW_16"]
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

#maxy_range = 100

if len(args) >= 7:
    y_axis_title = args[6]
else:
    y_axis_title = "% of loads marked"

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

if maxy_range - miny_range < 1.4:
    y_grid_interval = 0.1
elif maxy_range - miny_range < 2.4:
    y_grid_interval = 0.2
elif maxy_range - miny_range < 6.0:
    y_grid_interval = 0.5
elif maxy_range - miny_range < 15.0:
    y_grid_interval = 1.0
elif maxy_range - miny_range < 40.0:
    y_grid_interval = 2.0
elif maxy_range - miny_range < 100.0:
    y_grid_interval = 10.0
elif maxy_range - miny_range < 400.0:
    y_grid_interval = 20.0
else:
#    y_grid_interval = 10.0 ** (round(log(maxy_range- miny_range , 10)) - 1)
    y_grid_interval = 10.0 ** (round(log(maxy_range - miny_range , 10)) - 1)

def fix_serie(x):
    # removes useless decimals (x.0)
    try:
        if int(x) == float(x):
            return int(x)
    except:
        return x
    return x

series = [fix_serie(f) for f in sort_series(sorted_list_uniq([r[series_col] for r in data]))]
#series = ['NoFusion', 'RISCVFusion', 'CSF-SBR', 'RISCVFusion++','HELIOS', 'OracleFusion']
#series = ['CSF-SBR', 'RISCVFusion++', 'OracleFusion']
#series = ['NoFusion','Helios', 'OracleFusion']
#series = ['OracleFusion']
#series = ['AllFusion', 'MemFusion']
#series = ['AllFusion','MemFusion', 'OracleFusion']
#series = ['Helios', 'OracleFusion']
#series = ['TSO_56-72', 'COOL_20-40']
#series = ['BASE_72', 'COOL_52']
#series = ['BASE_128', 'COOL_64']
#series = ['BASE', 'COOL']
#series = ['generic', 'generic-fusion', 'macroop-fusion-inorder', 'macroop-fusion-inorder-v2', 'nofusion-o3', 'macroop-fusion-o3']

#series = ['OwnThreadLQSearch', 'OtherThreadsLQSearch', 'Invalidation&Evictions']

stackeds = [fix_serie(f) for f in sorted_list_uniq([r[stack_col] for r in data])]
#stackeds = ['Other', 'Memory']
#stackeds = ['M-search', 'D-search']
#stackeds =  ['OwnThreadLQSearch', 'OtherThreadsLQSearch', 'Invalidation&Evictions']

realapps = sorted_list_uniq([r[benchmark_col] for r in data])
apps = [i for i in realapps]
apps.append("/bAverage")
#apps.append("/bGeomean")

#Below you can change the x-axis size
if len(series) * len(apps) <= 20:
    frame_x = 100
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

if len(stackeds) <= 3:
    legend_rows = 1 #change the legend rows from here
else:
    legend_rows = 1

    legend_rows = 2
#below you can change the y-axis size
#MICRO22 graphs configuration
# frame_x = 280
# maxy_range = 30
# miny_range = 0
# y_grid_interval = 10
#frame_y = 25

#PACT22 Graphs configuration
frame_y = 45
frame_x = 100
y_grid_interval = 0.5

area_size = (mm_to_pt(frame_x), mm_to_pt(frame_y ))
#legend_x = 20 * ceil(len(stackeds)/legend_rows)
#legend_y = -5 # -2 # -1

if len(series) < 4:
    width_bars = (float(frame_x) / 1.5) / float(len(series) * len(apps))
else:
    width_bars = (float(frame_x) / 1.2) / float(len(series) * len(apps))
    

legend_x = 90 #Stalls [-- moves right] [++ moves left]
legend_y = 5 # Stall -8, DRF 0 [++ down] [--up]

legend_loc = (area_size[0] - mm_to_pt(legend_x), area_size[1] - mm_to_pt(legend_y))
x_axis_title = ""
def rgb(rx, gx, bx):
    return fill_style.Plain(bgcolor=color.T(r = rx / 256.0, g = gx / 256.0, b = bx / 256.0))

my_fill_style = (fill_style.gray20, fill_style.gray70, fill_style.diag, fill_style.gray50, fill_style.white, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)

my_fill_style2 = (fill_style.gray30, fill_style.gray70, fill_style.diag, fill_style.white, fill_style.rdiag, fill_style.vert, fill_style.gray30, fill_style.gray10)
rgb_fill_style_color = (rgb(94,79,162),rgb(50,136,150),rgb(102,194,165),rgb(171,221,164),rgb(230,245,152),rgb(255,255,191),rgb(254,224,139),rgb(253,174,97),rgb(244,109,67),rgb(213,62,79),rgb(158,1,66))

my_fill_style_color = (fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.lightyellow), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

if len(stackeds) == 2:
    #alexandra_fill_style_color = (fill_style.gray70, fill_style.red)
    alexandra_fill_style_color = (fill_style.Plain(bgcolor=color.red), fill_style.Plain(bgcolor=color.cornflowerblue))
    #alexandra_fill_style_color = (fill_style.red, fill_style.green)
    #alexandra_fill_style_color = (fill_style.green, fill_style.red)
else:
    alexandra_fill_style_color = (fill_style.red, fill_style.gray30, fill_style.Plain(bgcolor=color.cornflowerblue), fill_style.black, fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan))
    #alexandra_fill_style_color = (fill_style.Plain(bgcolor=color.snow),fill_style.Plain(bgcolor=color.black),fill_style.Plain(bgcolor=color.navy), fill_style.Plain(bgcolor=color.royalblue), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.limegreen), fill_style.Plain(bgcolor=color.yellow), fill_style.Plain(bgcolor=color.peru), fill_style.Plain(bgcolor=color.coral), fill_style.Plain(bgcolor=color.lightcoral), fill_style.Plain(bgcolor=color.red), fill_style.Plain(bgcolor=color.maroon), fill_style.Plain(bgcolor=color.khaki1), fill_style.Plain(bgcolor=color.gold4) )
    #alexandra_fill_style_color = (fill_style.gray30, fill_style.Plain(bgcolor=color.red), fill_style.Plain(bgcolor=color.cornflowerblue), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan))
    #alexandra_fill_style_color = (fill_style.red, fill_style.gray30, fill_style.gray50, fill_style.Plain(bgcolor=color.darkseagreen),fill_style.Plain(bgcolor=color.cornflowerblue), fill_style.red, fill_style.Plain(bgcolor=color.tan))
        
blas_fill_style_color = (fill_style.Plain(bgcolor=color.salmon), fill_style.Plain(bgcolor=color.darkseagreen2), fill_style.Plain(bgcolor=color.lightblue), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

#chronis_fill_style_color = (fill_style.Plain(bgcolor=color.brown), fill_style.Plain(bgcolor=color.goldenrod), fill_style.Plain(bgcolor=color.darkseagreen), fill_style.Plain(bgcolor=color.dodgerblue4), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)
chronis_fill_style_color = (fill_style.Plain(bgcolor=color.goldenrod), fill_style.Plain(bgcolor=color.brown), fill_style.Plain(bgcolor=color.darkseagreen), fill_style.Plain(bgcolor=color.dodgerblue4), fill_style.Plain(bgcolor=color.plum), fill_style.Plain(bgcolor=color.tan), fill_style.gray90)

y_axis_title = "/hC/12{" + y_axis_title + "}"

ar = area.T(size = area_size,
            x_coord = category_coord.T([[i] for i in apps], 0),
            y_range = (miny_range, maxy_range),
            y_grid_interval = y_grid_interval,
            x_axis = axis.X(label = x_axis_title, format="/12/hR/a40 %s"), #, format="/hR/a30 %s"
            y_axis = axis.Y(label = y_axis_title ,label_offset = (0,0), format="/12/hR/a0 %s"),
            legend = nodupslegend.T(nr_rows = legend_rows, loc = legend_loc ))

for serie_i in range(len(series)):
    prev_plot = None
    bar_plot.fill_styles.reset()
    print >> stderr, series[serie_i],
    sum_avg = 0
    for stack_j in range(len(stackeds)):
        serie_data = [(r[benchmark_col], r[data_col], r[data_col + 1]) for r in data if r[series_col] == series[serie_i] and r[stack_col] == stackeds[stack_j]]
        curr_apps = ([i[0] for i in serie_data])
        missing_apps = [i for i in realapps if i not in curr_apps]
        if missing_apps:
            m = [(i, 0.0, 0.0) for i in missing_apps]
            serie_data = serie_data + m
            serie_data.sort()

        if len([i[1] for i in serie_data]) > 0:
            serie_data.append(("/bAverage", average([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
            #serie_data.append(("/bGeomean", geomean([i[1] for i in serie_data]), average_error([i[2] for i in serie_data])));
            p = bar_plot.T(data = serie_data,
                           cluster = (serie_i, len(series)),
                           width = mm_to_pt(width_bars),
#                           fill_style = my_fill_style2[stack_j],
                           fill_style = alexandra_fill_style_color[stack_j],
                           #fill_style = rgb_fill_style_color[stack_j],
                           label = str(stackeds[stack_j]),
                           #error_bar = error_bar.bar2, error_minus_col = 2,
                           stack_on = prev_plot)
            ar.add_plot(p)
            prev_plot = p
            sum_avg += average([i[1] for i in serie_data])
            print >> stderr, stackeds[stack_j], average([i[1] for i in serie_data]),
    print  >> stderr, "=", sum_avg, "Impr:", round((1-sum_avg)*100,2), "%"
    #print >> stderr, series[serie_i], geomean([i[1] for i in serie_data])
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
            if serie_i == 1:
                # Here is placed left
                canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) - 16, ar.y_pos(ar.y_range[1]) - 10, "/hC/10{%.1f}" % value)
            elif serie_i == 2:
                # Here is placed right
                canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) + 20, ar.y_pos(ar.y_range[1]) - 10, "/hC/10{%.1f}" % value)
            else:
                # Here is placed up
                canvas.show(ar.x_pos(apps[serie_j]) - (((len(series) + 1) / 2) * mm_to_pt(width_bars)) + serie_i * mm_to_pt(width_bars) + 12, ar.y_pos(ar.y_range[1]) - 0, "/hC/10{%.1f}" % value)

#canvas.show(ar.x_pos(0), ar.x_pos(0), "/hC/12{%.2f}" % 83.3)


title_x = -20 #25
title_y = 6 # 6
legend_y = -2 #stalls # -5 #-2 #moves the legend to up or down
if title:
    title_text = "/hC/12{" + font.quotemeta(title) + "}"
    title_loc = ((area_size[0] - mm_to_pt(title_x)) / 2 - font.text_width(title_text) / 2, area_size[1] + mm_to_pt(title_y))
    tb = text_box.T(loc = title_loc, line_style = None, text = title_text)
    tb.draw()

if comment:
    comment_text = "/hc/12{" + font.quotemeta(comment) + "}"
    comment_loc = (mm_to_pt(-8), mm_to_pt(-25))
    tb = text_box.T(loc = comment_loc, line_style = None, text = comment_text)
    tb.draw()

if len(series) > 1:
    bars_pos = 10
    if len(series) < 4:
        legend_rows = len(series)
    elif len(series) % 6 == 0:
        legend_rows = 2
    elif len(series) % 5 == 0:
        legend_rows = 5
    elif len(series) % 3 == 0:
        legend_rows = 3
    elif len(series) % 2 == 0:
        legend_rows = 2
    else:
        legend_rows = 1
    legend_rows = 2 #it reflect the rows of legends that are generally in the top left corner of the graph
    index = 0
    bars_text = ""
    for i in series:
        bars_text = bars_text + str(index+1) + ". " + i + "\n"
        index = index + 1
        if (index % legend_rows) == 0:
            tb_bars = text_box.T(loc=(bars_pos,area_size[1] - mm_to_pt(legend_y) + 2), text=bars_text, line_style=line_style.gray70_dash1) #movement from here
            tb_bars.draw()
            bars_pos = bars_pos + font.get_dimension(bars_text)[1] + 14
            bars_text = ""

    while (index % legend_rows) != 0:
        bars_text = bars_text + " \n"
        index = index + 1
    if bars_text != "":
        tb_bars = text_box.T(loc=(bars_pos,area_size[1] - mm_to_pt(legend_y)), text=bars_text, line_style=line_style.gray70_dash1)
        tb_bars.draw()
    

