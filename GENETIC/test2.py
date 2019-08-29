from prob_g import ProblemGenerator
import util
import networkx as nx
import ssolver
import matplotlib.pyplot as plt
from matplotlib import animation
import time

test_instance =  'p4'
problem = ProblemGenerator().getByName(test_instance)

#alg = 'b'
#alg = 'h'
alg = 'g'

s1 = time.time()

if alg == 'b':

    moves = ssolver.solve_brute_force(problem.obstacles,
                                      problem.robot,
                                      problem.graph,
                                      problem.target)

    moves = ssolver.remove_jumps(moves)
    print('BRUTE FORCE:')
    print(moves)
    print('SOLVED IN  ' + str(len(moves)) + ' MOVES')


elif alg == 'h':

    moves = ssolver.solve_heap(problem.obstacles,
                               problem.robot,
                               problem.graph,
                               problem.target)

    print('\n\n')
    moves = ssolver.remove_jumps(moves)
    print('HEAP:')
    print(moves)
    print('SOLVED IN  ' + str(len(moves)) + ' MOVES')

elif alg == 'g':

    moves = ssolver.solve_genetic(problem.obstacles,
                                  problem.robot,
                                  problem.graph,
                                  problem.target)

    print('\n\n')
    #moves = ssolver.remove_jumps(moves)
    print('GENETIC:')
    print(moves)
    print('SOLVED IN  ' + str(len(moves)) + ' MOVES')



end = time.time()
print ("Time + " + str((end-s1)))


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

util.plt_show()


'''

if( 1 == 2):
    s1 = time.time()
#    moves = solver.solve_brute_force(problem)
    moves = ssolver.solve_brute_force(problem.obstacles,
                           problem.robot,
                           problem.graph,
                           problem.target)

    moves = ssolver.remove_jumps(moves)
    print('BRUTE FORCE:')
    print(moves)
    end = time.time()
    print ( "Time + " + str((end-s1)))

if 1 == 1:
    problem = ProblemGenerator().getByName(what)
    s1 = time.time()
    moves = ssolver.solve_heap(
        problem.obstacles,
        problem.robot,
        problem.graph,
        problem.target)

    print('\n\n')
    moves = ssolver.remove_jumps(moves)
    print('HEAP:')
    print('MOVES POSLE:')
    print(moves)
    end = time.time()
    print ( "Time + " + str((end-s1)))

if 1 == 2 :
    problem = ProblemGenerator().getByName(what)
    s1 = time.time()
    moves = solver.solve_genetic(problem)

    print('GENTIC:')
    print(moves)
    end = time.time()
    print ( "Time + " + str((end-s1)))
'''
