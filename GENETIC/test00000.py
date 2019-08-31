from prob_g import ProblemGenerator
import util
import networkx as nx
import ssolver
import matplotlib.pyplot as plt
from matplotlib import animation
import time

import operator

test_instance =  'p4'
problem = ProblemGenerator().getByName(test_instance)

o = ['a', 'a1', 't']
r = 's'



path = nx.shortest_path(problem.graph, problem.robot, problem.target)





obstacles_in_path = 0

for o in problem.obstacles:

    if o in path:
        obstacles_in_path += 1


chromosome_size = len(path) * obstacles_in_path


population_size = 100
initial_population = []

elite = 6

for i in range(population_size):
    initial_population.append(ssolver.create_random_path(problem.obstacles, problem.robot, problem.graph, problem.target, chromosome_size))

new_pop = []



for pop in initial_population:
    #print(pop)

    obstacles = problem.obstacles
    robot = problem.robot
    graph = problem.graph

    new_o, new_r = ssolver.make_moves(obstacles, robot, graph, pop)

    s = ssolver.score(pop, new_o, new_r, 't', graph)

    new_pop.append((s, pop ))


new_pop.sort(key = operator.itemgetter(0), reverse = True)

print('PARENTS: ')
print(new_pop[0])
print('\n')

print(new_pop[1])

print('\n\nCHILDREN')
child1, child2 = ssolver.crossover(new_pop[0], new_pop[1], problem.obstacles[:], problem.robot, problem.graph, problem.target)

print(child1)
print('\n')
print(child2)
