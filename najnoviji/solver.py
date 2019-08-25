import networkx as nx
import matplotlib.pyplot as plt

class Solver:
    def __init__(self,problem):
        self.problem = problem
        self.problem.graph=problem.graph.copy()

    def all_paths(self):
        return nx.all_simple_paths (self.problem.graph,
                                       self.problem.start ,
                                       self.problem.target,
                                       10000)


    def max_weight_matching(self,source,destination):
        bi_graph = self.bipartitive_graph(source,destination)
        return nx.max_weight_matching(bi_graph)

    def create_solution_graph(self,source,destination):
        graph = self.problem.graph.copy()
        matchs = self.max_weight_matching(source,destination)
        for match in matchs:
            graph.add_edge(match[0],match[1])
            graph.edges[match[0],match[1]]['color']='b'
        return graph
    
    def bipartitive_graph(self,source, destination):
        bi_graph = nx.Graph()
        g = self.problem.graph.copy()
        for source_node in source:
            if self.problem.is_obstacle(source_node):
                for dest_node in destination:
                    if self.problem.is_hole(dest_node):
                        shortest = nx.shortest_path(g, source_node, dest_node)
                        bi_graph.add_edge(source_node, dest_node, weight = 1000-len(shortest), shortest_path = shortest)

        return bi_graph

    def printnodes(self,dig):
        for node in dig.nodes():
            print(node)
            print( dig.nodes[node] )

    def nodename(self,node,i,prim):
        
        if(prim and i != 0 ):
            return node + '(' + str(i)+')p'
        return node+'('+str(i)+')'
    
        
    def solve_multi(self,graph,robots,targets,t):
        g = graph
        dig = nx.DiGraph()
        for node in graph.nodes():
            for i in range(t):
                demand=0
                if ( node in targets and node not in robots and i == t-1 ):
                    demand = 1
                else:
                    demand = 0
                if (node in robots and i == 0):
                    demand = -1
                dig.add_node(self.nodename(node,i,False),demand=0)
                dig.add_node(self.nodename(node,i,True),demand=demand)
        for node in dig.nodes():
            print(node)
            print( dig.nodes[node] )

        for edge in graph.edges():
            for i in range(t):
                node1prim = self.nodename(edge[0],i,True)
                node2prim = self.nodename(edge[1],i,True)
                node1plus = self.nodename(edge[0],i+1,False)
                node2plus = self.nodename(edge[1],i+1,False)

                n1 = edge[0]+edge[1]+str(i)+'_#1#';
                n2 = edge[0]+edge[1]+str(i)+'_#2#';
                dig.add_node(n1)
                dig.add_node(n2)
                         
                dig.add_edge(node1prim,n1, weight=0,capacity=1)
                dig.add_edge(node2prim,n1, weight=0,capacity=1)
                         
                dig.add_edge(n1,n2,weight=1,capacity=1)
                
                dig.add_edge(n2,node1plus,weight=0,capacity=1)
                dig.add_edge(n2,node2plus,weight=0,capacity=1)
                
                
        for node in graph.nodes():
            dig.add_edge( self.nodename(node,0,False),self.nodename(node,1,False) ,weight=1,capacity = 1,color='g')
            dig.add_edge( self.nodename(node,1,False),self.nodename(node,1,True), weight=0,capacity = 1,color='b')                    
            for i in range(t):
                if i > 0 :
                    dig.add_edge(self.nodename(node,i-1,True),self.nodename(node,i,False), weight=1,capacity = 1,color='g')
                    dig.add_edge(self.nodename(node,i-1,False),self.nodename(node,i,True), weight=1,capacity = 1,color='b')                    
        return dig
        
