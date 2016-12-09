#!/usr/bin/env python3

import argparse
import json
import re

parser = argparse.ArgumentParser(description="A helper script to generate Mathematica's GraphPlot function from json.")
parser.add_argument("json", help="the file to graph")
parser.add_argument("-l", "--min-links", help="only nodes with more then MIN_LINKS edges will be shown. (default: 0)", type=int, default=0)
parser.parse_args()
args = parser.parse_args()
output = "GraphPlot[{"

hosts = json.loads(open(args.json).read())

for host in hosts:
  r_host = re.sub(r'^http[s]?://', '', host)
  for child in hosts[host]:
    r_child = re.sub(r'^http[s]?://', '', child)
    if not hosts.get(child) and args.min_links > 0: continue
    if (hosts.get(child) and len(hosts.get(child)) <= args.min_links) or len(hosts.get(host)) <= args.min_links: continue
    if r_host != r_child: output += '"' + r_host + '" -> "' + r_child + '",'

output += "}, VertexLabeling -> True]"

print(re.sub(',}','}', output))
