#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
import signal
import json
import argparse

parser = argparse.ArgumentParser(description="Trace link tree.")
parser.add_argument("url", help="the url to start trace")
parser.add_argument("outfile", help="path to save json")
parser.add_argument("-d", "--depth", help="max depth to go (default: 10)", type=int, default=10)
parser.add_argument("-t", "--timeout", help="timeout when fetching a page (default: 5)", type=int, default=5)
parser.parse_args()
args = parser.parse_args()

route = {}
max_depth = args.depth
max_time = args.timeout

def ltrace(url, depth): 
  print(" " * depth + "> " + url)
  if(depth >= max_depth): return
  try:
    this_html = urlopen(url, timeout=max_time)
    this_soup = BeautifulSoup(this_html, "lxml")
    for l in this_soup.findAll('a', attrs={'href': re.compile("^http[s]?://")}):
      this_link = l.get('href')
      this_host = re.match('^http[s]?://[^/]*', this_link).group(0)
      if this_link == this_host or this_host + "/" == this_link: 
        if not route.get(url): route[url] = []
        if this_host in route[url]: return
        route[url].append(this_host)
        ltrace(this_host, depth+1)
  except Exception:
    print(" " * depth + "< " + url + " (urllib error)")
    return
  print(" " * depth + "< " + url)
  return

def save(string): 
  f = open(args.outfile, 'wt', encoding='utf-8')
  f.write(string)

try:
  ltrace("http://nat.moe", 0)
except KeyboardInterrupt:
  save(json.dumps(route))
  sys.exit()
save(json.dumps(route))
