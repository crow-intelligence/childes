import json
from collections import Counter

from bounter import bounter
import networkx as nx
from nltk.util import skipgrams

stoplist = ["trn", "vocalizes"]
with open("data/json/clean.json", "r") as infile:
    month_utterances = json.load(infile)

nodes = []
months = []
for k, v in month_utterances.items():
    months.append(int(k))
    for e in v:
        e = e.split()
        for wd in e:
            nodes.append(wd)
months = sorted(months)
nodes = Counter(nodes)
nodes = {k: v for k, v in sorted(nodes.items(), key=lambda item: item[1]) if
         v > 500 and (len(k) > 1 or k == "a") and k not in stoplist}
vocabulary = set(nodes.keys())
print(len(vocabulary))

wd_times = {}
edges = bounter(size_mb=1024)
i = len(vocabulary)
for wd in vocabulary:
    print(f"remains {i} words")
    times = []
    for k,v in month_utterances.items():
        for e in v:
            e = e.split()
            e = [w for w in e if w in vocabulary]
            if len(e) > 1:
                if wd in set(e):
                    times.append(int(k))
                skips = list(skipgrams(e, 2, 3))
                skips = [skip[0] + "_" + skip[1] for skip in skips]
                edges.update(skips)
    if len(times) > 0:
        sdate = min(times)
        edate = max(times)
        t = (sdate, edate)
        wd_times[wd] = t
    i -= 1

G = nx.Graph()
for k,v in wd_times.items():
    G.add_node(k, start=v[0], end=191)

total = edges.total()
for e in edges.items():
    fromwd, towd = e[0].split("_")
    weight = int(e[1]) / total
    # and weight > 0.00005
    if fromwd in wd_times and towd in wd_times:
        G.add_edge(fromwd, towd, weight=weight)

nx.write_graphml(G, "data/graphml/childes.graphml")
