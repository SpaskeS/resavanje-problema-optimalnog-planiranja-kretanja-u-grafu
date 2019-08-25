# -*- coding: utf-8 -*-
"""
Class to generate problems
nodes is set of nodes
edges is tuples of string 
obstacles is list of strings where is obstacles
start,target is strings with 
name is name of predifined problem 
"""




import networkx as nx
import matplotlib.pyplot as plt
import problem_generator as pg

class Problem:

    def __init__(self,nodes=None,edges=None,
                 obstacles=None,start=None,
                 target=None):
        self.graph = nx.Graph()
        self.robot = start
        self.start = start
        self.target = target
        self.obstacles = []
        for node in nodes:
            self.graph.add_node(node)
        for edge in edges:
            self.graph.add_edge(edge[0],edge[1])
        self.obstacles = obstacles
        for node in self.graph.nodes():
            self.graph.nodes[node]['color'] = self.color(node)
    def is_obstacle(self,node):
        return node in self.obstacles
        
    def is_hole(self,node):
        if node not in self.obstacles:
            return True

    def color(self,node):
        if (node in self.obstacles and node == self.target):
            return 'c'
        if node in self.obstacles:
            return 'r'
        if node == self.robot:
            return 'b'
        if node == self.start:
            return 'y'
        if node == self.target:
            return 'g'
        return 'w'

                         
        
            
