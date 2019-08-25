from prob_g import ProblemGenerator
import util
import networkx as nx
from solver import Solver
import matplotlib.pyplot as plt
from matplotlib import animation

problem = ProblemGenerator().getByName('p1')

'''
print(problem)


problem.move_obstacle('f', 'd')
problem.move_robot('s', 'y')
problem.move_robot('y', 'x')
util.plt_graph(problem.graph)

moves = [('s', 'y')]
problem.moves(moves)

util.plt_graph(problem.graph)
'''


paths = nx.all_simple_paths (problem.graph,
                            problem.robot ,
                            problem.target,
                            10000)

print('all paths:')
for path in paths:
    print(path)

solver = Solver(problem, path)

print('all possible moves: ')
print(solver.possible_moves())

moves = solver.solve_brute_force(problem, path)
print('BRUTE FORCE:')
print(moves)


#util.plt_graph(problem.graph)
#util.plt_show()

pos = nx.spring_layout(problem.graph)

def set_colors():
    colors = []
    for node1 in problem.graph.nodes:
        colors.append(problem.color(node1))
    return colors

def init():
    #nx.draw_networkx(problem.graph, pos=pos, with_labels=True, node_color=set_colors(), font_weight='bold'   )
    return

def move(m):
    source = m[0]
    dest = m[1]
    if source == problem.robot:
        problem.robot = dest

    if source in problem.obstacles:
        problem.obstacles.remove(source)
        problem.obstacles.append(dest)


def animate(i):

    if i > 0:
        move(moves[i-1])
    ax.clear()
    nx.draw_networkx(problem.graph, pos=pos,  with_labels=True, node_color=set_colors(), font_weight='bold')


fig, ax = plt.subplots(figsize=(6,4))
ani = animation.FuncAnimation(fig, animate, frames=len(moves)+1, init_func=init,
                              interval=1000, repeat=False)

util.plt_show()
