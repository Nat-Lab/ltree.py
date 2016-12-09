#!/usr/bin/env python3

import argparse
import json
import re

parser = argparse.ArgumentParser(description="A helper script to generate Mathematica's GraphPlot function from json.")
parser.add_argument("json", help="the file to graph")
parser.parse_args()
args = parser.parse_args()
output = "GraphPlot[{"

hosts = json.loads(open(args.json).read())

for host in hosts:
  r_host = re.sub(r'^http[s]?://', '', host)
  for child in hosts[host]:
    r_child = re.sub(r'^http[s]?://', '', child)
    if (r_host != r_child): output += '"' + r_host + '" -> "' + r_child + '",'

output += "}, VertexLabeling -> True]"

print(re.sub(',}','}', output))
