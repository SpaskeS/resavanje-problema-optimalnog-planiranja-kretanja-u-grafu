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


def create_state(o, r):

    o.sort()
    return '-'.join(o) + ' ___ R = ' + r

#__________________________________________________________________________________

def fitness_fun_heap(graph, obstacles, robot, target, num_of_moves):
    shortest = nx.shortest_path(graph,robot,target)
    score = -len(shortest) - num_of_moves

    for obstacle in obstacles:
        if obstacle in shortest:
            score = score - 1

    return -score



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
            score = fitness_fun_heap(graph,obstacles,robot,t,len(moves))
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
    num_of_solutions = 0
    all_solutions = []

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
                    #print("FOUND SOLUTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    all_solutions.append(new_moves)
                    #return new_moves

                round = round+1

                if (round % 100000 == 0):
                    print ("Visited = " + str(len(visited)))
                queue.append((new_moves,newobstacles,newrobot))


    print('Number of solutions: ' + str(len(all_solutions)))

    min_len = float('inf')
    best = all_solutions[0]

    for i in range(len(all_solutions)):
        if len(all_solutions[i]) < min_len:
            min_len = len(all_solutions[i])
            best = all_solutions[i]

    return best

'''
____________ GENETIC ____________

'''

ELITE = 9
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.85
MAX_GENERATION_NUMBER = 100
TOURNAMENT_SIZE = 7
REPRODUCTION_SIZE = 200
CHROMOSOME_LEN = 100
GENERATION_SIZE = 1000


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

    return selected


def crossover(parent1, parent2, o, r, graph):

    return


def mutation(moves):
    return

def create_new_generation(selected, graph, t):

    return chromosomes



def score(gene, t, graph):

    ((o, robot, state, moves), weight) = gene


    shortest = nx.shortest_path(graph, robot, t)
    score =  -len(shortest) - weight

    if robot == t:
        score += 10000 - weight

    for obstacle in o:
        if obstacle in shortest:
            score = score - 1

    return score


def print_solution(chromosome, t):

    for c in chromosome:
        if c[1][1] == t:
            print('solution score: ' + str(c[0]))
            print('solution obs: ' + str(c[1][0]))
            print('solution robot: ' + str(c[1][1]))
            print('solution state: ' + str(c[1][2]))
            print('solution moves: ' + str(c[1][3]))
            print('solution weight: ' + str(c[2]))


def num_of_solutions_in_chromosome(chromosome, t):

    tnum = 0

    for c in chromosome:
        if c[1][1] == t:
            tnum += 1

    #print('broj resenja: ' + str(tnum))
    return tnum


def print_chr(chromosome, t):
    i = 0

    for c in chromosome:

        i += 1
        print(str(i) + 'th: ')
        print('score: ' + str(c[0]))
    #    print('obs: ' + str(c[1][0]))
        print('robot: ' + str(c[1][1]))
    #    print('state: ' + str(c[1][2]))
        print('moves: ' + str(c[1][3]))
        print('weight: ' + str(c[2]))


def create_chromosome(o, r, graph, t):

    n = len(o) + 1
    state = create_state(o, r)
    states = [state]

    moves = []
    obstacles = o[:]
    robot = r
    weight = 0

    g = ((obstacles, robot, states, moves), weight)
    fitness = score(g, t, graph)

    gene = (fitness, (obstacles, robot, states, moves), weight)

    chromosome = [gene]

    solved = False

    while len(chromosome) != CHROMOSOME_LEN:

        pm = possible_moves(obstacles, robot, graph)

        random_move =  random.choice(pm)

        random_m = random_move[3][:2]

        if len(moves) > 0:

            last_move = moves[-1][3][:2]
            last_move.reverse

        else:
            last_move = '#'


        if random_m != last_move or len(moves) == 0:
            #print('USAO')
            new_o, new_r = make_move(obstacles, robot, graph, random_move[0], random_move[1])
            #print('DODAJE POTEZ ' + str(random_move))
            new_state = create_state(new_o, new_r)

            if new_state not in states:

                new_moves = moves[:]
                new_moves.append(random_move)

                new_states = states[:]
                new_states.append(new_state)

                new_weight = weight + random_move[2]

                new_fitness = score(((new_o, new_r, new_states, new_moves), weight), t, graph)

                chromosome.append((new_fitness, (new_o, new_r, new_states, new_moves), new_weight))

                moves = new_moves[:]
                obstacles = new_o[:]
                robot = new_r
                weight = new_weight
                states = new_states[:]
                state = new_state
                states = new_states[:]

                if new_r == t:
                    
                    print('RESIO')
                    solved = True
                    break

            else:
                #print('OSTAJE ISTO')
                new_fitness = score(((obstacles, robot, states, moves), weight), t, graph)
                chromosome.append((new_fitness, (obstacles, robot, states, moves), weight))


    if solved:

        while len(chromosome)  != CHROMOSOME_LEN:
            chromosome.append((new_fitness, (obstacles, robot, states, moves), weight))




    return chromosome


def initial_population(o, r, graph, t):

    init_population = []

    for i in range(100):
        init_population.append(create_chromosome(o[:], r, graph, t))

    return init_population


def fitness_fun(chromosome):

    fitness = 0

    for c in chromosome:
        if num_of_solutions_in_chromosome(c) == 0:

            bad_chromosome = copy.copy(c)




def solve_genetic(o, r, graph, t):

    population = initial_population(o, r, graph, t)

    for i in range(len(population)):
        #print_chr(population[i], t)
        num = num_of_solutions_in_chromosome(population[i], t)
        print(num)
        k  =1

    return 1




'''
#    print('\n\n')
#    print('WINNER : ' + str(tournament_selection(initial, graph, t)))
#    print('\n\nSELECTED FROM SELECTION:')
#    for selected in selected_chromosomes:
#        print(selected)

#    print('NEW GENERATION: ')
#    for c in new_generation:

#        print(c)

#    print('NEW generation size: ' + str(len(new_generation)))



    for chromosome in population:
        score = fitness_fun(graph, o, r, t, len(chromosome))

    while generations_number < GENERATION_NUMBER:



        generetaions_number += 1
'''
