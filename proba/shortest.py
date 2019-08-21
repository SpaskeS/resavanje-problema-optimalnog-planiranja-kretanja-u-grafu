import networkx as nx
import math
import heapq
from cvorKlasa import Cvor

def get_node_by_name(g, name):
    for node in list(g.nodes):
        if node.name == name:
            return node
    return None

def dijekstra(g,start,end):
    dist = {}
    prev = {}
    Q = set()
    h = []
    for node in list(g.nodes):
        dist[node] = 100000
        prev[node] = None
        Q.add(node)

    dist[start] = 0
    for key in dist.keys():
        heapq.heappush(h,(dist[key],key))
    while(len(h) > 0):
        n = heapq.heappop(h)[1]
        for neighbor in g[n].keys():
            alt=dist[n] + 1
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = n
    path = [end]
    k = end
    while(k!=start):
        print(k)
        path.insert(0,prev[k])
        k = prev[k]
    return path
