from prob_g import ProblemGenerator
import util
import networkx as nx
from solver import Solver

problem = ProblemGenerator().getByName('p2')

print(problem)

util.plt_graph(problem.graph)

'''
problem.move_obstacle('f', 'd')
problem.move_robot('s', 'y')
problem.move_robot('y', 'x')
util.plt_graph(problem.graph)
'''

#moves = [('s', 'y')]
#problem.moves(moves)

#util.plt_graph(problem.graph)

paths = nx.all_simple_paths (problem.graph,
                            problem.robot ,
                            problem.target,
                            10000)

for path in paths:
    print(path)

solver = Solver(problem, path)
#util.plt_graph(solver.graph)

print(solver.possible_moves())

moves = solver.solve(problem, path)


ani = animation.FuncAnimation(fig, animate, frames=len(moves), init_func = init, interval=400, repeat=False)



#print(solver.find_nearest_hole(problem.graph, 't'))
