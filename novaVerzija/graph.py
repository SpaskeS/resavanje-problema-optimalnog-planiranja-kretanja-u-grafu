import networkx as nx
import matplotlib.pyplot as plt
from cvorKlasa import Cvor
import functions as f

from matplotlib import animation

def get_node_by_name(g, name):
    for node in list(g.nodes):
        if node.name == name:
            return node
    return None

def path_str(path):
    s = ''
    for node in path:
        s = s + node.name
    return s


def makeGraph(nodes, edges, obstacles):
    g = nx.Graph()

    for node in nodes:
        c = Cvor(node, node in obstacles, node == 's')
        g.add_node(c)

    for edge in edges:
        source = get_node_by_name(g, edge[0])
        dest = get_node_by_name(g, edge[1])
        g.add_edge(source, dest)

    return g

def set_colors(g):
    colors = []
    for node1 in g.nodes:
        colors.append(node1.color())
    return colors

def move(m,g):
    source = get_node_by_name(g, m[0])
    dest = get_node_by_name(g, m[1])
    dest.robot = source.robot

    dest.obstacle = source.obstacle
    source.robot = False
    source.obstacle = False
