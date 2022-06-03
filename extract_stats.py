#!/usr/bin/python2.7

# script.py path_to_search string_to_find stats_position_in_that_line dir_to_csv_file
# python extract_stats.py /home/sawan/echo/llvm-pass-results/ *generic-fusion-rv64-stats.log "Total_CI:" 1 $(pwd)/
# python extract_stats.py /home/sawan/echo/PolyBenchC-4.2.1/output/ *macroop-fusion-o3-rv64-stats.log "Total_CI:" 1 $(pwd)/ normal LLVM graph "% of instr"

from email.mime import application
from lib2to3.pytree import WildcardPattern
import sys
import glob
import csv
from collections import Counter
import shlex, subprocess
import math
from fnmatch import fnmatch

path = sys.argv[1]
WildcardPattern = sys.argv[2]
string = sys.argv[3]
extract_point = sys.argv[4]
csv_file = sys.argv[5]
graph_type = sys.argv[6]
config_vary = sys.argv[7]

pdf_name = sys.argv[8]
y_axis_name = sys.argv[9]
max = sys.argv[10]
min = sys.argv[11]

file_to_open = path + WildcardPattern
csv_path = csv_file + 'log.csv'
csv_path_sorted = csv_file + 'log_sorted.csv'
f_csv = open(csv_path, 'w')


def read_param (f, p):
  with open(filename, 'r') as f:
    for line in f:
      if line.startswith(p):
        final = (line.split(p)[int(extract_point)])
        final = final.split()[0]
        return final
    raise AttributeError

is_config = ""
config_list = []

#get all the config possible
for filename in glob.glob(file_to_open):
  if (read_param(filename,config_vary) != is_config):
    is_config = read_param(filename,config_vary)
    if (len(config_list) == 0):
      config_list.append(is_config)
    else:
      new = True
      for vary in config_list:
        if (vary == is_config):
          new = False
      if (new):
          config_list.append(is_config)

print (config_list)

#start generating the csv file from below
if (graph_type == "normal"):
  for filename in glob.glob(file_to_open):
    application = read_param(filename, "SIMULATION_BENCHMARK:")
    get_value = read_param(filename, string)
    f_csv.write(read_param(filename, config_vary))
    f_csv.write(',')
    f_csv.write(application)
    f_csv.write(',')
    f_csv.write(str(get_value))
    f_csv.write(',')
    f_csv.write('0.0')
    f_csv.write('\n')


sort_command = "cat " + csv_path + " | sort -k1,1 -t ','  > " + csv_path_sorted + " \n"
cat_command = "cat " + csv_path + " | sort -k1,1 -t ','" + "\n"

subprocess.Popen(cat_command, shell=True)
subprocess.Popen(sort_command, shell=True)

if (graph_type == "normal"):
  plot = "./plot/plot-bars.py 0 1 2" + ' "" ' + '"" ' + '"' + y_axis_name + '"' + " " + max + " " + min + " < ./log_sorted.csv > pdf/" + pdf_name + ".pdf" + "\n"

print(plot)
subprocess.Popen(plot, shell=True)

