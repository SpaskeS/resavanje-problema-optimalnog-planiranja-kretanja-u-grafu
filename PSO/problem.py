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
import prob_g as pg

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

    def move_robot(self, node_from, node_to):
        if not node_from == self.robot:
            raise RuntimeError('node_from is not robot ' + node_from)

        if node_to in self.obstacles:
            raise RuntimeError('node_to is obstacle ' + node_to)

        self.robot = node_to
        self.refresh([node_from, node_to])

    def move_obstacle(self, node_from, node_to):
        self.obstacles.append(node_to)
        self.obstacles.remove(node_from)
        self.refresh([node_to, node_from])

    def move(self, node_from, node_to):
        if self.robot == node_from:
            self.move_robot(node_from, node_to)
            return

        if node_from in self.obstacles:
            self.move_obstacle(node_from, node_to)
            return

        raise RuntimeError('Cant move from ' + node_from)

    def moves(self, moves):
        for move in moves:
            self.move(move[0], move[1])

    def refresh(self, nodes):
        for node in nodes:
            self.graph.nodes[node]['color'] = self.color(node)
