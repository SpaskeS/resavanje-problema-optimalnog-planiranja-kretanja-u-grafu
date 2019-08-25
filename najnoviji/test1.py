import problem as prbl
import problem_generator as pgen
import solver
import networkx as nx
import matplotlib.pyplot as plt
import util as util

problem = pgen.ProblemGenerator.getByName(name="p2")

util.plt_graph(problem.graph)

solver = solver.Solver(problem)

#for path in  solver.all_paths():
    # source = []
    # for node in problem.graph.nodes():
    #     if problem.is_obstacle(node):
    #         source.append(node)
    # dest = []
    # for node in problem.graph.nodes():
    #     if ( node not in path and problem.is_hole(node) ):
    #         dest.append(node)
    # bi = solver.bipartitive_graph(source,dest)
#    util.plt_graph(bi)

#   sol = solver.create_solution_graph(source,dest)
starts =  ['s']
targets = ['t']

dig = solver.solve_multi(problem.graph,starts,targets,2)
print ("Nodes " + str(len(dig.nodes)))
util.plt_graph(dig)
flowCost,flowDict = nx.capacity_scaling(dig)


# d1 = nx.DiGraph()


# solver.add_merge_split(d1,('A','B'),1)
# util.plt_graph(d1)
    



   
