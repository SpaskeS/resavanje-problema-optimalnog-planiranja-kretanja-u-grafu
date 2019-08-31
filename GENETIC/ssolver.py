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

    if node_from == None:
        return (o, r)

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


def different_moves(move1, move2):

    first1 = move1[0]
    first2 = move1[1]

    second1 = move2[0]
    second2 = move2[1]

    if first1 == second2 and first2 == second1:
        return False

    return True



def score(chromosome, o, robot, t, graph):

    shortest = nx.shortest_path(graph, robot, t)

    weight = 0

    for i in range(len(chromosome)):
        weight += chromosome[i][2]

    score =  -len(shortest) - weight

    if robot == t:
        score += 10000


    for obstacle in o:
        if obstacle in shortest:
            score = score - 10

    return score



def create_random_path(o, r, graph, t, chromosome_len):

    moves = []
    new_o = o[:]
    new_r = r
    visited = set()

    visited_times = 0

    solved = False

    while(len(moves) < chromosome_len):

        solved = False

        pm = possible_moves(new_o, new_r, graph)

        random_move = random.choice(pm)

        diff = True

        if len(moves) > 0:
            last_move = moves[-1]

            if different_moves(random_move, last_move):
                diff = True
            else:
                diff = False

        if diff:
            tmp_o = new_o
            tmp_r = new_r

            new_o, new_r = make_move(new_o, new_r, graph, random_move[0], random_move[1])


            new_visited = create_state(new_o, new_r)


            if new_visited not in visited:

                new_moves = moves[:]
                new_moves.append(random_move)

                visited.add(new_visited)
                moves = new_moves
                if new_r == t:
                    solved = True
                    print('RESIO')
                    print(new_moves)
                    break



                visited_times = 0

            else:

                visited_times +=1

                new_o = tmp_o
                new_r = tmp_r
                if visited_times > 100:
                    solved = True
                    break


    if solved:
        while len(moves) < chromosome_len:
            moves.append((None, None, 0, []))


    return moves

def crossover(parent1, parent2, o, r, graph, t):

    (score1, moves1) = parent1
    (score2, moves2) = parent2

    obstacles = o[:]
    robot = r

    i = random.randint(0, len(moves1))

    print('I: ' + str(i))
    new_moves = moves1[:i]
    new_o, new_r = make_moves(obstacles, robot, graph, new_moves)

    for j in range(i, len(moves2)):

        if moves2[j] in possible_moves(new_o, new_r, graph):
            new_moves.append(moves2[j])
            new_o, new_r = make_move(new_o, new_r, graph, moves2[j][0], moves2[j][1])
            if new_r == t:
                break


#    print('LEN NEW MOVES: ' + str(len(new_moves)))

    if new_r != t:
        rest_of_path = create_random_path(new_o, new_r, graph, t, len(moves1) - len(new_moves))
        new_moves.extend(rest_of_path)


    else:
        while len(new_moves) < len(moves1):
            new_moves.append((None, None, 0, []))

    child1_o, child1_r = make_moves(o[:], r, graph, new_moves)
    child_score1 = score(new_moves, child1_o, child1_r, t, graph)

    child1 = (child_score1, new_moves)


    new_moves_2 = moves2[:i]
    new_o_2, new_r_2 = make_moves(o[:], r, graph, new_moves_2)

    for j in range(i, len(moves2)):

        if moves1[j] in possible_moves(new_o_2, new_r_2, graph):
            new_moves_2.append(moves1[j])
            new_o_2, new_r_2 = make_move(new_o_2, new_r_2, graph, moves1[j][0], moves1[j][1])

            if new_r_2 == t:
                break


#    print('LEN NEW MOVES 2: ' + str(len(new_moves_2)))

    if new_r_2 != t:
        rest_of_path = create_random_path(new_o_2, new_r_2, graph, t, len(moves1) - len(new_moves_2))
        new_moves_2.extend(rest_of_path)


    else:
        while len(new_moves_2) < len(moves1):
            new_moves_2.append((None, None, 0, []))


    child2_o, child2_r = make_moves(o[:], r, graph, new_moves_2)
    child_score2 = score(new_moves_2, child2_o, child2_r, t, graph)

    child2 = (child_score2, new_moves_2)

    return child1, child2





def selection(chromosomes, graph, target):

    selected = []

    return selected


def create_new_generation(selected, graph, t):

    return chromosomes





def fitness_fun(chromosome):

    return



def solve_genetic(o, r, graph, t):

    oves = create_random_path(o, r, graph, t)
    print(oves)




    return 1
