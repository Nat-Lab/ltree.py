#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request
import re
import sys
import signal
import json
import argparse
import traceback

parser = argparse.ArgumentParser(description="Trace link tree.")
parser.add_argument("url", help="the url to start trace")
parser.add_argument("outfile", help="path to save json")
parser.add_argument("-d", "--depth", help="max depth to go (default: 10)", type=int, default=10)
parser.add_argument("-t", "--timeout", help="timeout when fetching a page (default: 5)", type=int, default=5)
parser.add_argument("-a", "--alexa", help="min alexa of site to be shown (so you don't get trapped into big sites (e.g. twitter/facebook)) (default: unlimited)", type=int, default=-1)
parser.add_argument("-i", "--ignore", help="domain keywords to exclude, separate mutiple keywords by comma", default="")
parser.parse_args()
args = parser.parse_args()

route = {}
alexa = {}
max_depth = args.depth
max_time = args.timeout

def urlopen(url, timeout=5): 
  req = urllib.request.Request(url, data=None, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14' })
  return urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8')

def alexa_check(host):
  if args.alexa <= 0: return True
  if alexa.get(host): return alexa.get(host) > args.alexa
  html = urlopen("http://data.alexa.com/data?cli=10&url=" + host)
  soup = BeautifulSoup(html, "lxml")
  if soup.find("reach"): rank = int(soup.find("reach").get("rank"))
  else: rank = args.alexa + 1
  alexa[host] = rank
  return rank > args.alexa

def keyword_check(host):
  for word in args.ignore.split(","):
    if word != "" and word.lower() in host: return False
  return True

def check(host):
  host = re.sub(r'^http[s]?://', '', host)
  return keyword_check(host) and alexa_check(host)

def ltrace(url, depth): 
  print(" " * depth + "> " + url)
  if not check(url): 
    print(" " * depth + "< " + url + " (check does not pass)")
    return
  if depth >= max_depth: return
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
  except Exception as err:
    print(" " * depth + "< " + url + " (got Exception)")
    return
  print(" " * depth + "< " + url)
  return

def save(string): 
  f = open(args.outfile, 'wt', encoding='utf-8')
  f.write(string)

try:
  ltrace(args.url, 0)
except KeyboardInterrupt:
  save(json.dumps(route))
  sys.exit()
save(json.dumps(route))
