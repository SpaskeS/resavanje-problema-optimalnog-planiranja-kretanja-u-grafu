import heapq as heap
import networkx as nx
import copy
import random

def remove_jumps(moves):

    res = []

    for move in moves:
        if move[2] > 1:
            move[3].reverse()
            res.extend(make_moves_from_path(move[3]))
        else:
            res.append(move)

    return res


def make_moves_from_path(path):

    moves = []
    p = path[:]

    for i in range(len(p)-1):
        moves.append((p[i+1], p[i], 1, [p[i+1], p[i]]))
    return moves


def find_nearest_hole(o,r,graph, start):
    visited, queue = [], [(start, [start])]
    results = []

    while queue:
        (node, search_path) = queue.pop(0)

        if node not in visited:
            visited.append(node)
            adjacent = graph.adj[node]
            for neighbor in adjacent:
                if neighbor in o:
                    if neighbor not in visited:
                        queue.append((neighbor, search_path + [neighbor]))
                else:
                    if neighbor != r:
                        results.append(search_path + [neighbor])

    moves = []
    for res in results:

        moves.append((res[0], res[-1], len(res)-1, res))
    return moves

def move_robot(o,r,graph,node_from,node_to):
    obstacles = o[:]
    robot = r
    if not node_from == r:
        raise RuntimeError('node_from is not robot ' + node_from)

        if node_to in obstacles:
            raise RuntimeError('node_to is obstacle ' + node_to)
    robot = node_to
    return (obstacles,robot)

def move_obstacle(o,r,graph,node_from,node_to):
    obstacles = o[:]
    robot  = r
    if node_from not in obstacles:
        raise RuntimeError('node_from is not obstacle ' + node_from)
    if node_to in obstacles:
        raise RuntimeError('node_to is obstacle ' + node_to)

    if node_to == robot:
        raise RuntimeError('node_to is robot' + node_to)

    obstacles.append(node_to)
    obstacles.remove(node_from)

    return(obstacles,robot)

def make_move(o,r,graph,node_from,node_to):
    if( r == node_from):
        return move_robot(o,r,graph,node_from,node_to)
    if ( node_from in o):
        return move_obstacle(o,r,graph,node_from,node_to)

    raise RuntimeError('Cant move from ' + node_from)

def make_moves(o,r,graph,moves):
    obstacles=o[:]
    robot = r
    for move in moves:
        obstacles,robot = make_move(obstacles,robot,graph,move[0],move[1])
    return (obstacles,robot)

def is_hole(o, r, node):
    if (node not in o):
        return True
    return False

def possible_robot_moves(o, r, graph):
    moves=[]
    robot_node = r
    robot_neighbors = graph.adj[r]

    for neighbor in robot_neighbors:
        if is_hole(o,r,neighbor):
            moves.append((robot_node, neighbor, 1, [robot_node, neighbor]))
    return moves

def possible_obstacle_moves(o,r,graph,obstacle):
    obstacle_neighbors =  graph.adj[obstacle]
    moves = []

    for neighbor in obstacle_neighbors:
        if is_hole(o,r,neighbor) and neighbor != r:
            moves.append((obstacle, neighbor, 1, [obstacle, neighbor]))
        else:
            if neighbor != r:
                moves.extend(find_nearest_hole(o,r,graph, neighbor))

    return moves

def possible_obstacles_moves(o,r,graph):
    moves = []
    for obstacle in o:
        moves.extend(possible_obstacle_moves(o,r,graph,obstacle))
    return moves

def possible_moves(o,r,graph):
    moves = []
    moves.extend(possible_robot_moves(o,r,graph))
    moves.extend(possible_obstacles_moves(o,r,graph))
    return moves


def color(o,r,graph,node,target,start):
        if (node in o and node == target):
            return 'c'
        if node in o:
            return 'r'
        if node == r:
            return 'b'
        if node == start:
            return 'y'
        if node == target:
            return 'g'
        return 'w'



def solve_heap(o,r,graph,t):
    round = 0
    visited = set([])
    queue= [(-1000,[],o,r)]
    while queue:
        score,moves,obstacles,robot = heap.heappop(queue)
        obstacles.sort()
        st = ('#'.join(obstacles),robot)
        if ( st not in visited ):
            visited.add(st)
            score = fitness_fun(graph,obstacles,robot,t,len(moves))
            pm = possible_moves(obstacles,robot,graph)

            for move in pm:
                new_moves = moves[:]
                new_moves.append(move)
                newobstacles,newrobot = make_moves(obstacles,robot,graph,[move])
                if t == newrobot:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return new_moves

                round = round+1
                if (round % 100000 == 0):
                    print ("Visited = " + str(len(visited)))
                heap.heappush(queue,(score,new_moves,newobstacles,newrobot))

def solve_brute_force(o,r,graph,t):
    round = 0
    visited = set([])
    queue = [([],o,r)]
    while queue:
        moves,obstacles,robot = queue.pop(0)
        obstacles.sort()
        st = ('#'.join(obstacles),robot)
        if ( st not in visited ):
            visited.add(st)

            pm = possible_moves(obstacles,robot,graph)
            for move in pm:
                new_moves = moves[:]
                new_moves.append(move)
                newobstacles,newrobot = make_moves(obstacles,robot,graph,[move])
                if t == newrobot:
                    print("f!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return new_moves
                round = round+1
                if (round % 100000 == 0):
                    print ("Visited = " + str(len(visited)))
                queue.append((new_moves,newobstacles,newrobot))


def create_state(o, r):

    o.sort()
    return '#'.join(o) + '__________' + r


ELITE = 9
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.9
MAX_GENERATION_NUMBER = 100
TOURNAMENT_SIZE = 5
REPRODCTION_SIZE = 10


def fitness_fun(graph, obstacles, robot, target, num_of_moves):
    shortest = nx.shortest_path(graph,robot,target)
    score = -len(shortest) - num_of_moves

    for obstacle in obstacles:
        if obstacle in shortest:
            score = score - 1

    return -score


def tournament_selection(chromosomes, graph, target):

    winner = None
    tournament_size = min(TOURNAMENT_SIZE, len(chromosomes))

    selected = random.sample(chromosomes, tournament_size)

    best_score = float('inf')

    for s in selected:
        obstacles, robot, moves, state_set = s
        move_length = 0
        for move in moves:
            move_length += move[2]

        score = fitness_fun(graph, obstacles, robot, target, move_length)

        if score < best_score:
            winner = s
            best_score = score

    return winner, best_score


def selection(chromosomes, graph, target):

    selected = []
    print('len: ' + str(len(chromosomes)))
    for i in range(REPRODCTION_SIZE):
        winner, score = tournament_selection(chromosomes, graph, target)
        selected.append(winner)

    return selected


def crossover(parent1, parent2, o, r, graph):

    o1, r1, moves1, state_set1 = parent1
    o2, r2, moves2, state_set2 = parent2

    break_point = random.randrange(1, len(moves1))
    child1_moves = []
    child2_moves = []

    new_o = o[:]
    new_r = r

    child1_state_set = set()
    child2_state_set = set()

    initial_state = create_state(new_o, new_r)

    child1_state_set.add(initial_state)
    child2_state_set.add(initial_state)

    for i in range(0, break_point):

        new_o, new_r = make_move(new_o, new_r, graph, moves1[i][0], moves1[i][1])
        new_state = create_state(new_o, new_r)
        if new_state not in child1_state_set:
            child1_state_set.add(new_state)
            child1_moves.append(moves1[i])

    pm = possible_moves(new_o, new_r, graph)

    for i in range(break_point, len(moves2)):
        if moves2[i] in pm:
            new_o, new_r = make_move(new_o, new_r, graph, moves2[i][0], moves2[i][1])
            new_state = create_state(new_o, new_r)
            if new_state not in child1_state_set:
                child1_state_set.add(new_state)
                child1_moves.append(moves2[i])
                pm = possible_moves(new_o, new_r, graph)


    child1 = (new_o, new_r, child1_moves, child1_state_set)

    return child1


def mutation(moves):
    return

def create_generation(selected, graph, t):

    chromosomes = []

    for s in selected:
        o, r, moves, state_set = s

        pm = possible_moves(o, r, graph)

        for move in pm:

            new_moves = moves[:]
            new_state_set =  copy.copy(state_set)
            new_obstacles, new_robot = make_move(o, r, graph, move[0], move[1])

            new_state = create_state(new_obstacles, new_robot)
            if new_state not in new_state_set:

                new_moves.append(move)
                new_state_set.add(new_state)

                new_c = (new_obstacles, new_robot, new_moves, new_state_set)

                chromosomes.append(new_c)

    return chromosomes

def initial_population(chromosome, graph, t):

    chromosomes = []

    (o, r, moves, state_set) = chromosome

    pm = possible_moves(o, r, graph)

    for move in pm:
        new_moves = moves[:]
        new_state_set =  copy.copy(state_set)
        new_obstacles, new_robot = make_move(o, r, graph, move[0], move[1])
        new_moves.append(move)

        new_state = create_state(new_obstacles, new_robot)
        new_state_set.add(new_state)

        new_c = (new_obstacles, new_robot, new_moves, new_state_set)

        chromosomes.append(new_c)

    return chromosomes

def solve_genetic(o, r, graph, t):

    generations_number = 0
    state_set = set()

    state = create_state(o, r)

    state_set.add(state)
    chromosome = (o[:], r, [], state_set)

    initial = initial_population(chromosome, graph, t)

    solved = False
    while generations_number < 60 or solved == True:
        if generations_number == 0:
            selected = selection(initial, graph, t)
        else:
            selected = selection(population, graph, t)

        population = create_generation(selected, graph, t)

        for p in population:
            obs, rob, moves, state_set = p
            if rob == t:
                solved = True
                print('kRA')
                print(p)
                return


        generations_number += 1


    print('parent1:')
    print(population[0])

    print('\n\nparent2: ')
    print(population[1])

    print('\nchild:')
    print(crossover(population[0], population[1], o, r, graph))
    print(generations_number)


#    print('\n\n')
#    print('WINNER : ' + str(tournament_selection(initial, graph, t)))

    selected_chromosomes = selection(initial, graph, t)
#    print('\n\nSELECTED FROM SELECTION:')
#    for selected in selected_chromosomes:
#        print(selected)

    new_generation = create_generation(selected_chromosomes, graph, t)
#    print('NEW GENERATION: ')
#    for c in new_generation:

#        print(c)

#    print('NEW generation size: ' + str(len(new_generation)))


    return 1

'''
    for chromosome in population:
        score = fitness_fun(graph, o, r, t, len(chromosome))

    while generations_number < GENERATION_NUMBER:



        generetaions_number += 1
'''
