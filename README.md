ltree.py: 鏈接樹
---


`ltree.py` 是一個用於追蹤站點間鏈接的腳本。用法如下：

```
usage: ltree.py [-h] [-d DEPTH] [-t TIMEOUT] [-a ALEXA] [-i IGNORE]
                url outfile

Trace link tree.

positional arguments:
  url                   the url to start trace
  outfile               path to save json

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        max depth to go (default: 10)
  -t TIMEOUT, --timeout TIMEOUT
                        timeout when fetching a page (default: 5)
  -a ALEXA, --alexa ALEXA
                        min alexa of site to be shown (so you don't get
                        trapped into big sites (e.g. twitter/facebook))
                        (default: unlimited)
  -i IGNORE, --ignore IGNORE
                        domain keywords to exclude, separate mutiple keywords
                        by comma

```

附帶一個小工具，用於轉換輸出的 json 到 Mathematica 的 GraphPlot。

```
usage: graph.py [-h] json

A helper script to generate Mathematica's GraphPlot function from json.

positional arguments:
  json        the file to graph

optional arguments:
  -h, --help  show this help message and exit
```
