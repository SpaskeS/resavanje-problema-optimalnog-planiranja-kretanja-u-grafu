import networkx as nx
import math
import heapq 

""" From https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
function Dijkstra(Graph, source):
o  create vertex set Q 
    for each vertex v in Graph:             // Initialization
      dist[v] ← INFINITY                  // Unknown distance from source to v
        prev[v] ← UNDEFINED                 // Previous node in optimal path from source
        add v to Q                          // All nodes initially in Q (unvisited nodes)
      dist[source] ← 0                        // Distance from source to source
      while Q is not empty:
            u ← vertex in Q with min dist[u]    // Node with the least distance will be selected first
            remove u from Q 
          
          for each neighbor v of u:           // where v is still in Q.
              alt ← dist[u] + length(u, v)
              if alt < dist[v]:               // A shorter path to v has been found
                  dist[v] ← alt 
                  prev[v] ← u 

      return dist[], prev[]
"""

def dijekstra(g,start,end):
    dist = {}
    prev = {}
    Q = set()
    h = []
    for node in list(g.nodes):
        dist[node] = 100000
        prev[node] = None
        Q.add(node)
        
    dist['s'] = 0
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
        path.insert(0,prev[k])
        k = prev[k]
    return path

