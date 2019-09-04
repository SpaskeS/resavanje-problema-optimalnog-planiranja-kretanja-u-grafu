from prob_g import ProblemGenerator
import util
import networkx as nx
import ssolver
import genetic
import matplotlib.pyplot as plt
from matplotlib import animation
import time
import problem as prbl
from prozor import Prozor

#prozor = Prozor()
# prozor.root.mainloop()
# p = prozor.get_p()
# problem = prbl.Problem(nodes=p["nodes"],
#                     edges=p["edges"],
#                     start=p["start"],
#                     target=p["target"],
#                     obstacles=p["obstacles"]
# )
# algorithm = prozor.get_algoritam()

algorithm = 'g'
problem = ProblemGenerator().getByName('p9')

path = nx.shortest_path(problem.graph, problem.robot, problem.target)
s = time.time()

if algorithm == 'b':

    moves = ssolver.solve_brute_force(problem.obstacles,
                                      problem.robot,
                                      problem.graph,
                                      problem.target)

    moves = ssolver.remove_jumps(moves)
    print('BRUTE FORCE:')
    print(moves)
    print('SOLVED IN  ' + str(len(moves)) + ' MOVES')
    end = time.time()
    print ("Time + " + str((end-s)))


elif algorithm == 'h':

    moves = ssolver.solve_heap(problem.obstacles,
                               problem.robot,
                               problem.graph,
                               problem.target)

    print('\n\n')
    moves = ssolver.remove_jumps(moves)
    print('HEAP:')
    print(moves)
    print('SOLVED IN  ' + str(len(moves)) + ' MOVES')
    end = time.time()
    print ("Time + " + str((end-s)))

elif algorithm == 'g':

    moves = genetic.solve_genetic(problem.obstacles,
                                  problem.robot,
                                  problem.graph,
                                  problem.target,
                                  path)

    if len(moves) == 0:
        moves = ssolver.solve_brute_force(problem.obstacles,
                                          problem.robot,
                                          problem.graph,
                                          problem.target)


    moves = ssolver.remove_jumps(moves)
    print('GENETIC: ')
    print(moves)
    print('SOLVED IN  ' + str(len(moves)) + ' MOVES')

    end = time.time()
    print ("Time + " + str((end-s)))



pos = nx.spring_layout(problem.graph)

def set_colors():
    colors = []
    for node1 in problem.graph.nodes:
        colors.append(problem.color(node1))
    return colors

def init():
    nx.draw_networkx(problem.graph, pos=pos, with_labels=True, node_color=set_colors(), font_weight='bold'   )
    print('init')

def move(m):
    source = m[0]
    dest = m[1]
    if source == problem.robot:
        problem.robot = dest

    if source in problem.obstacles:
        problem.obstacles.remove(source)
        problem.obstacles.append(dest)


def animate(i):
    ax.clear
    if(i > 0 ):
        move(moves[i-1])
    nx.draw_networkx(problem.graph, pos=pos,  with_labels=True, node_color=set_colors(), font_weight='bold'   )


fig, ax = plt.subplots(figsize=(6,4))
ani = animation.FuncAnimation(fig, animate, frames=len(moves)+1, init_func=init,
                              interval=1000, repeat=False)
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
util.plt_show()
