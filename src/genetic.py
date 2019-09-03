from prob_g import ProblemGenerator
import util
import networkx as nx
import ssolver
import random
import copy
import operator

test_instance =  'p7'
problem = ProblemGenerator().getByName(test_instance)

def different_moves(move1, move2):

    first1 = move1[0]
    first2 = move1[1]

    second1 = move2[0]
    second2 = move2[1]

    if first1 == second2 and first2 == second1:
        return False

    return True

def create_random_path(o, r, graph, t, chromosome_len):

    moves = []
    new_o = copy.deepcopy(o)
    new_r = r
    visited = set()

    visited_times = 0

    solved = False
    no_more_states = False

    while(len(moves) < chromosome_len):

        solved = False
        no_more_states = False

        pm = ssolver.possible_moves(new_o, new_r, graph)

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

            new_o, new_r = ssolver.make_move(new_o, new_r, graph, random_move[0], random_move[1])
            new_visited = ssolver.create_state(new_o, new_r)

            if new_visited not in visited:

                new_moves = copy.deepcopy(moves)
                new_moves.append(random_move)

                visited.add(new_visited)
                moves = new_moves
                if new_r == t:
                    solved = True
                    break

                visited_times = 0

            else:
                visited_times +=1

                new_o = tmp_o
                new_r = tmp_r
                if visited_times > 100:
                    no_more_states = True
                    break

    return moves
'''
    if solved:
        return moves
        #while len(moves) < chromosome_len:
        #    moves.append(('1', '1', 0, []))

    if no_more_states:
        return moves
    #    while len(moves) < chromosome_len:
    #        moves.append(('0', '0', 0, []))
'''




def create_initial_population(o, r, graph, t, chromosome_size, population_size):

    obstacles = copy.deepcopy(o)
    robot = r

    initial_population = []
    for i in range(population_size):
        new_chromosome = create_random_path(obstacles, robot, graph, t, chromosome_size)

        initial_population.append(new_chromosome)

    return initial_population

def fitness_fun(chromosome, o, r, graph, t, path):

    last_robot = None
    for i in range(1, len(chromosome)):
        if chromosome[-i][1] == r:
            last_robot = chromosome[-i][0]
            break

    weight = 0
    obstacles = copy.deepcopy(o)

    for i in range(len(chromosome)):
        weight += chromosome[i][2]

    score = - weight

    if r == t:
        score += 10000

    for node in path:
        if node == r:
            distance = nx.shortest_path_length(graph, r, t)
            for obstacle in obstacles:
                if obstacle in path:
                    distance-=1
            score += 10*((len(path)-distance+1))

    count_obs = 0

    for obstacle in obstacles:

        if obstacle in path:
            count_obs += 1
            obs_distance = nx.shortest_path_length(graph, obstacle, t)
            score = score - 40*count_obs - 5*(len(path)-obs_distance+1)
            # if last_robot != None and nx.shortest_path_length(graph, r, t) > nx.shortest_path_length(graph, last_robot, t):
            #     score += count_obs*40

    if ssolver.is_hole(obstacles, r, t) and count_obs == 0:
        # distance = nx.shortest_path_length(graph, r, t)
        # score += 70*(len(path)-distance+1)
        score += 5000


    return score

#     winner_move = ('1', '1', 0, [])
#     loser_move = ('0', '0', 0, [])
#
#     counter_res = chromosome.count(winner_move)
#
#     for move in chromosome:
#         if move == winner_move:
#             score += 10
#             break
#
#         if move == loser_move:
#             score -= 50
#             break


def fit_chromosome(chromosome_moves, o, r, graph, population_size, path, t):

    obstacles = copy.deepcopy(o)
    robot = r

    chromosome_o, chromosome_r = ssolver.make_moves(obstacles, robot, graph, chromosome_moves)

    fitness = fitness_fun(chromosome_moves, chromosome_o, chromosome_r, graph, t, path)
    scored_chromosome = ((fitness, chromosome_moves))

    return scored_chromosome
'''
    if ('1', '1', 0, []) in chromosome_moves:
        index_winner = chromosome_moves.index(('1', '1', 0, []))
        chromosome_o, chromosome_r = ssolver.make_moves(obstacles, robot, graph, chromosome_moves[:index_winner])

    elif ('0', '0', 0, []) in chromosome_moves:
        index_loser = chromosome_moves.index(('0', '0', 0, []))
        chromosome_o, chromosome_r = ssolver.make_moves(obstacles, robot, graph, chromosome_moves[:index_loser])
'''




def tournament_selection(population, tournament_size):

    winner = None
    tournament = random.sample(population, tournament_size)

    winner = max(tournament, key=lambda item:item[0])

    return winner


def selection(population, reproduction_size, tournament_size):

    selected = []

    while len(selected) < reproduction_size:
        selected.append(tournament_selection(population, tournament_size))

    return selected

def create_new_generation(population, selected, population_size, elite_size, o, r, graph, t, path):

    new_generation = sorted(population, key= lambda item:item[0], reverse=True)[:int(elite_size)]

    while len(new_generation) < population_size:

        valid_parents = False
        while(valid_parents == False):
            parent1, parent2 = random.sample(selected, 2)

            if len(parent1[1]) > 5 and len(parent2[1]) > 5:
                child1 = crossover(parent1, parent2, o, r, graph, t, population_size, path)
                valid_parents = True


        if random.randrange(0, 100) < 3:

            mutated_child = mutation(child1, o, r, graph, population_size, path, t)
            new_generation.append(mutated_child)
        else:
            new_generation.append(child1)

    return new_generation


def mutation(chromosome, o, r, graph, population_size, path, t):

    moves = chromosome[1]
    print(chromosome[1])
    obstacles = copy.deepcopy(o)
    robot = r
    new_o, new_r = ssolver.make_moves(obstacles, robot, graph, moves)

    pm = ssolver.possible_moves(new_o, new_r, graph)

    for p in pm:
        if different_moves(p, moves[-1]):
            moves.append(p)
            break

    new_o, new_r = ssolver.make_moves(copy.deepcopy(o), r, graph, moves)

    mutated = fit_chromosome(moves, copy.deepcopy(o), r, graph, population_size, path, t)

    return mutated

def crossover(parent1, parent2, o, r, graph, t, population_size, path):

    (score1, moves1) = parent1
    (score2, moves2) = parent2

    obstacles = copy.deepcopy(o)
    robot = r

    if len(moves1) <= len(moves2):

        i = random.randrange(1, len(moves1)-1)
        new_moves =  moves1[:i]

    else:

        i = random.randrange(1, len(moves2)-1)
        new_moves = moves2[:i]

    new_o, new_r = ssolver.make_moves(obstacles, robot, graph, new_moves)

    if len(moves1) <= len(moves2):
        for j in range(i, len(moves2)):

            if moves2[j] in ssolver.possible_moves(new_o, new_r, graph) and different_moves(moves2[j], new_moves[-1]):
                new_moves.append(moves2[j])
                new_o, new_r = ssolver.make_move(new_o, new_r, graph, moves2[j][0], moves2[j][1])
                if new_r == t:
                    break

    else:
        for j in range(0, len(moves1)):
            if moves1[j] in ssolver.possible_moves(new_o, new_r, graph) and different_moves(moves1[j], new_moves[-1]):
                new_moves.append(moves1[j])
                new_o, new_r = ssolver.make_move(new_o, new_r, graph, moves1[j][0], moves1[j][1])
                if new_r == t:
                    break



    child1 = fit_chromosome(new_moves, obstacles, robot, graph, population_size, path, t)
    return child1

'''    if len(moves1) <= len(moves2):

        for j in range(i, len(moves2)):

            if moves2[j] in ssolver.possible_moves(new_o, new_r, graph) and different_moves(moves2[j], new_moves[-1]):
                new_moves.append(moves2[j])
                new_o, new_r = ssolver.make_move(new_o, new_r, graph, moves2[j][0], moves2[j][1])
                if new_r == t:
                    break

    elif len(moves1) > len(moves2):
        for j in range(0, len(moves2)):
            if moves2[j] in ssolver.possible_moves(new_o, new_r, graph) and different_moves(moves2[j], new_moves[-1]):
                new_moves.append(moves2[j])
                new_o, new_r = ssolver.make_move(new_o, new_r, graph, moves2[j][0], moves2[j][1])'''

    # TODO mozda nw trbea newo i ewr


'''    new_moves_2 = moves2[:k]
# !!!!

    new_o_2, new_r_2 = ssolver.make_moves(obstacles, robot, graph, new_moves_2)


    if len(moves2) <= len(moves1):
        for j in range(k, len(moves1)):
            if moves1[j] in ssolver.possible_moves(new_o_2, new_r_2, graph) and different_moves(moves1[j], new_moves_2[-1]):

                new_moves_2.append(moves1[j])
                new_o_2, new_r_2 = ssolver.make_move(new_o_2, new_r_2, graph, moves1[j][0], moves1[j][1])

                if new_r_2 == t:
                    break
    else:
        for j in range(0, len(moves1)):
            if moves1[j] in ssolver.possible_moves(new_o_2, new_r_2, graph) and different_moves(moves1[j], new_moves_2[-1]):
                new_moves.append(moves1[j])
                new_o_2, new_r_2 = ssolver.make_move(new_o_2, new_r_2, graph, moves1[j][0], moves1[j][1])

    child2 = fit_chromosome(new_moves_2, obstacles, robot, graph, population_size, path, t)

    return child1, child2'''


'''
    if new_r != t:
    #    while len(new_moves) < len(moves1):

    #        appended, app_o, app_r = random_move(new_moves, new_o, new_r, graph, t)
    #        if appended == [] and app_o == [] and app_r == '':
    #            child1 = parent1
    #            break
    #        new_moves.append(appended)
    #        new_o = app_o[:]
    #        new_r = app_r


    else:
        while len(new_moves) < len(moves1):

            new_moves.append(('1', '1', 0, []))
'''

'''
    if new_r_2 != t:
        while len(new_moves_2) < len(moves1):

            appended2, app_o2, app_r2 = random_move(new_moves_2, new_o_2, new_r_2, graph, t)

            if appended2 == [] and app_o2 == [] and app_r2 == '':
                child2 = parent2
                break

            new_moves_2.append(appended2)
            new_o_2 = app_o2[:]
            new_r_2 = app_r2


    else:
        while len(new_moves_2) < len(moves1):
            new_moves_2.append(('1', '1', 0, []))
'''

'''
    if ('1', '1', 0, []) in new_moves_2:
        index_winner = new_moves_2.index(('1', '1', 0, []))
        new_o_2, new_r_2 = ssolver.make_moves(obstacles, robot, graph, new_moves_2[:index_winner])

    elif ('0', '0', 0, []) in new_moves_2:
        index_loser = new_moves_2.index(('0', '0', 0, []))
        new_o_2, new_r_2 = ssolver.make_moves(obstacles, robot, graph, new_moves_2[:index_loser])
'''

'''
    if ('1', '1', 0, []) in new_moves:
        index_winner = new_moves.index(('1', '1', 0, []))
        new_o, new_r = ssolver.make_moves(obstacles, robot, graph, new_moves[:index_winner])

    elif ('0', '0', 0, []) in new_moves:
        index_loser = new_moves.index(('0', '0', 0, []))
        new_o, new_r = ssolver.make_moves(obstacles, robot, graph, new_moves[:index_loser])
'''

def random_move(current_moves, o, r, graph, t):

    initial_obs = problem.obstacles[:]
    initial_r = problem.robot

    moves = copy.deepcopy(current_moves)
    obstacles = o[:]
    robot = r

    counter = 0
    visited_states = set()

    for move in current_moves:
        if move != ('1', '1', 0, []) and move != ('0', '0', 0, []):
            move_o, move_r = ssolver.make_move(initial_obs, initial_r, graph, move[0], move[1])
            state = ssolver.create_state(move_o, move_r)
            visited_states.add(state)
            initial_obs = move_o[:]
            initial_r = move_r

    keep_looking = True

    while keep_looking == True:

        pm = ssolver.possible_moves(obstacles, robot, graph)
        if len(pm) == 0:
            raise RuntimeError('PRAZA PM')

        random_move = random.choice(pm)

        if len(moves) > 0:
            last_move = moves[-1]

            if different_moves(last_move, random_move):
                new_move = random_move[:]
                new_o, new_r = ssolver.make_move(obstacles, robot, graph, new_move[0], new_move[1])
                new_state = ssolver.create_state(new_o, new_r)

                if new_state not in visited_states:

                    return new_move, new_o, new_r

                else:

                    i = 0
                    for p in pm:
                        i += 1
                        if i == len(pm):
                            keep_looking = False

                        new_move = p[:]
                        new_o, new_r = ssolver.make_move(obstacles, robot, graph, new_move[0], new_move[1])
                        new_state = ssolver.create_state(new_o, new_r)

                        if new_state not in visited_states:

                            return new_move, new_o, new_r

    if keep_looking == False:
        return [], [], ''


def solve_genetic(o, r, graph, t, path):

    obstacles_in_path = 0

    for obs in o:
        if obs in path:
            obstacles_in_path += 1

    chromosome_size = len(path) * obstacles_in_path
    population_size = 100
    elite_size = population_size / 5
    max_iterations = 50
    reproduction_size = 20
    tournament_size = 5

    initial_population = create_initial_population(o, r, graph,
                                                   t, chromosome_size, population_size)

    scored_population = []
    for i in range(population_size):

        chromosome = initial_population[i]
        scored_population.append(fit_chromosome(chromosome, o, r, graph, population_size, path, t))

    current_pop = copy.deepcopy(scored_population)

    for i in range(max_iterations):
        selected = selection(current_pop, reproduction_size, tournament_size)
        current_pop = create_new_generation(current_pop, selected, population_size, elite_size,
                                            o, r, graph, t, path)

        print(current_pop[0])
        best = max(current_pop, key=lambda item:item[0])
        print(str(i) + ' : ' + str(best))


    print('BEST ' + str(best))

    return best[1]
