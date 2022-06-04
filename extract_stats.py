#!/usr/bin/python2.7

# script.py path_to_search string_to_find stats_position_in_that_line dir_to_csv_file
# python extract_stats.py /home/sawan/echo/llvm-pass-results/ *generic-fusion-rv64-stats.log "Total_CI:" 1 $(pwd)/
# python extract_stats.py /home/sawan/echo/PolyBenchC-4.2.1/output/ *macroop-fusion-o3-rv64-stats.log "Total_CI:" 1 $(pwd)/ normal LLVM graph "% of instr"
# ./extract_stats.py llvm_total_ci_per normal_percentage /home/sawan/echo/PolyBenchC-4.2.1/output/ *stats.log "LLVM_CONFIG:" "% of instr" 10 0

from email.mime import application
from lib2to3.pytree import WildcardPattern
import sys
import glob
import csv
from collections import Counter
import shlex
import subprocess
import math
from fnmatch import fnmatch
import os

plot_graph = sys.argv[1]
graph_type = sys.argv[2]
path = sys.argv[3]
WildcardPattern = sys.argv[4]
config_vary = sys.argv[5]
y_axis_name = sys.argv[6]
max = sys.argv[7]
min = sys.argv[8]

file_to_open = path + WildcardPattern
csv_path = os.getcwd() + "/csv/" + 'log.csv'
csv_path_sorted = os.getcwd() + "/csv/" + 'log_sorted.csv'

normal_stats = [
    ("llvm_exec_instrs", "Total_instructions_in_deptrace:"),
    ("llvm_total_ci", "Total_CI:"),
]
normal_percentage_stats = [
    ("llvm_total_ci_per", "Total_CI:", "Total_instructions_in_deptrace:"),
]
stacked_stats = [
    ("total_fusion",
     ("CI", "Total_CI:"),
     ("NCI", "Total_NCI:"),
     ("Total_instructions_in_deptrace:")),
]
stacked_percentage_stats = [
    ("total_fusion_per",
     2,
     ("CI", "Total_CI:"),
     ("NCI", "Total_NCI:"),
     ("Total_instructions_in_deptrace:")),

    ("total_ci_per",
     3,
     ("CI", "CI_CA_SSR:"),
     ("SL", "CI_SL_SSR:"),
     ("NL", "CI_NL_SSR:"),
     ("Total_instructions_in_deptrace:")),
]

if (graph_type == "normal"):
    for s in normal_stats:
        if (s[0] == plot_graph):
            stat_to_plot = s
            break

if (graph_type == "normal_percentage"):
    for s in normal_percentage_stats:
        if (s[0] == plot_graph):
            stat_to_plot = s
            break

if (graph_type == "stacked"):
    for s in stacked_stats:
        if (s[0] == plot_graph):
            stat_to_plot = s
            break

if (graph_type == "stacked_percentage"):
    for s in stacked_percentage_stats:
        if (s[0] == plot_graph):
            stat_to_plot = s
            break

if (stat_to_plot == ""):
    raise AttributeError

f_csv = open(csv_path, 'w')


def read_param(f, p):
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(p):
                final = (line.split(p)[int(1)])
                final = final.split()[0]
                return final
        raise AttributeError


is_config = ""
config_list = []
# get all the config possible
for filename in glob.glob(file_to_open):
    if (read_param(filename, config_vary) != is_config):
        is_config = read_param(filename, config_vary)
        if (len(config_list) == 0):
            config_list.append(is_config)
        else:
            new = True
            for vary in config_list:
                if (vary == is_config):
                    new = False
            if (new):
                config_list.append(is_config)

print(config_list)

# start generating the csv file from below
if (graph_type == "normal"):
    for filename in glob.glob(file_to_open):
        application = read_param(filename, "SIMULATION_BENCHMARK:")
        get_value = read_param(filename, stat_to_plot[1])
        f_csv.write(read_param(filename, config_vary))
        f_csv.write(',')
        f_csv.write(application)
        f_csv.write(',')
        f_csv.write(str(get_value))
        f_csv.write(',')
        f_csv.write('0.0')
        f_csv.write('\n')

if (graph_type == "normal_percentage"):
    for filename in glob.glob(file_to_open):
        application = read_param(filename, "SIMULATION_BENCHMARK:")
        get_value = float(read_param(filename, stat_to_plot[1]))
        base_value = float(read_param(filename, stat_to_plot[2]))
        get_value = get_value / base_value * 100.0000
        f_csv.write(read_param(filename, config_vary))
        f_csv.write(',')
        f_csv.write(application)
        f_csv.write(',')
        f_csv.write(str(get_value))
        f_csv.write(',')
        f_csv.write('0.0')
        f_csv.write('\n')

if (graph_type == "stacked_percentage"):
    for filename in glob.glob(file_to_open):
        for stacked in range(stat_to_plot[1]):
            application = read_param(filename, "SIMULATION_BENCHMARK:")
            get_value = float(read_param(
                filename, stat_to_plot[stacked + 2][1]))
            base_value = float(read_param(
                filename, stat_to_plot[stat_to_plot[1] + 2]))
            get_value = get_value / base_value * 100.0000
            f_csv.write(read_param(filename, config_vary))
            f_csv.write(',')
            f_csv.write(application)
            f_csv.write(',')
            f_csv.write(stat_to_plot[stacked + 2][0])
            f_csv.write(',')
            f_csv.write(str(get_value))
            f_csv.write(',')
            f_csv.write('0.0')
            f_csv.write('\n')

sort_command = "cat " + csv_path + \
    " | sort -k1,1 -t ','  > " + csv_path_sorted + " \n"
cat_command = "cat " + csv_path + " | sort -k1,1 -t ','" + "\n"

os.system(cat_command)
os.system(sort_command)

pdfcrop = "pdfcrop ./pdf/" + stat_to_plot[0] + ".pdf ./pdf/" + stat_to_plot[0] + ".pdf"
pdfopen = "evince ./pdf/" + stat_to_plot[0] + ".pdf &"

if (graph_type == "normal" or graph_type == "normal_percentage"):
    plot = "./plot/plot-bars.py 0 1 2" + ' "" ' + '"" ' + '"' + y_axis_name + '"' + \
        " " + max + " " + min + " < ./csv/log.csv > pdf/" + \
        stat_to_plot[0] + ".pdf" + "\n"

if (graph_type == "stacked" or graph_type == "stacked_percentage"):
    plot = "./plot/plot-bars-stacked.py 0 2 1 3" + ' "" ' + '"" ' + '"' + y_axis_name + '"' + \
        " " + max + " " + min + " < ./csv/log.csv > pdf/" + \
        stat_to_plot[0] + ".pdf && " + pdfcrop + " && " + pdfopen + "\n"

print(plot)

os.system(plot)

