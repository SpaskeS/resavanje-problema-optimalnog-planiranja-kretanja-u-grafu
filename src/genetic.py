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
#
#    for c in chromosome:
#        if c[2] > 1:
#            score += c[2]*10

    for obstacle in obstacles:
        if obstacle in path:
            count_obs += 1
            obs_distance = nx.shortest_path_length(graph, obstacle, t)
            score = score - 40*count_obs - 5*(len(path)-obs_distance+1)

    if ssolver.is_hole(obstacles, r, t) and count_obs == 0:
        distance = nx.shortest_path_length(graph, r, t)
        score += 1000*(len(path)-distance+1)


    #    score += 5000

    return score

def fit_chromosome(chromosome_moves, o, r, graph, population_size, path, t):

    obstacles = copy.deepcopy(o)
    robot = r

    chromosome_o, chromosome_r = ssolver.make_moves(obstacles, robot, graph, chromosome_moves)

    fitness = fitness_fun(chromosome_moves, chromosome_o, chromosome_r, graph, t, path)
    scored_chromosome = ((fitness, chromosome_moves))

    return scored_chromosome


def tournament_selection(population, tournament_size):
    pop = copy.deepcopy(population)

    winner = None
    tournament = []
    for i in range(tournament_size):
        c = random.choice(pop)
        tournament.append(c)

    winner = max(tournament, key=lambda item:item[0])

    return winner


def selection(population, reproduction_size, tournament_size):

    pop = copy.deepcopy(population)
    selected = []

    while len(selected) < reproduction_size:
        selected.append(tournament_selection(pop, tournament_size))

    return selected

def create_new_generation(elite, selected, population_size, elite_size, o, r, graph, t, path):

    new_generation = copy.deepcopy(elite)

    while len(new_generation) < population_size:

        valid_parents = False
        while(valid_parents == False):
            parent1, parent2 = random.sample(selected, 2)

            if len(parent1[1]) > 5 and len(parent2[1]) > 5:
                child1 = crossover(parent1, parent2, o, r, graph, t, population_size, path)
                valid_parents = True


        if random.randrange(0, 100) < 10:

            mutated_child = mutation(child1, o, r, graph, population_size, path, t)
            new_generation.append(mutated_child)
        else:
            new_generation.append(child1)

    return new_generation


def mutation(chromosome, o, r, graph, population_size, path, t):

    moves = chromosome[1]

    obstacles = copy.deepcopy(o)
    robot = r
    new_o, new_r = ssolver.make_moves(obstacles, robot, graph, moves)

    pm = ssolver.possible_moves(new_o, new_r, graph)

    for p in pm:
        #different_moves(p, moves[-1]) and
        if p[0] == new_r:

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


def solve_genetic(o, r, graph, t, path):

    obstacles_in_path = 0

    for obs in o:
        if obs in path:
            obstacles_in_path += 1

    chromosome_size = len(path) * obstacles_in_path

    population_size = 100
    elite_size = 50
    max_iterations = 100
    reproduction_size = 30
    tournament_size = 10

    initial_population = create_initial_population(o, r, graph,
                                                   t, chromosome_size, population_size)

    scored_population = []
    for i in range(population_size):

        chromosome = initial_population[i]
        scored_population.append(fit_chromosome(chromosome, o, r, graph, population_size, path, t))

    current_pop = copy.deepcopy(scored_population)

    for i in range(max_iterations):

        #elite = sorted(copy.deepcopy(current_pop), key= lambda item:item[0], reverse=True)[:int(elite_size)]
        elite = []
        for_selection = copy.deepcopy(current_pop)
        for j in range(elite_size):
            largest = max(for_selection, key=lambda item:item[0])
            elite.append(largest)
            for_selection.remove(largest)

#        for_selection = copy.deepcopy(current_pop)
#        for s in for_selection:
#            if s in elite:
#                for_selection.remove(s)

        selected = selection(for_selection, reproduction_size, tournament_size)

        current_pop = create_new_generation(elite, selected, population_size, elite_size,
                                            o, r, graph, t, path)


        best = max(current_pop, key=lambda item:item[0])
        print(str(i) + ' : ' + str(best))


    print('BEST ' + str(best))

    return best[1]
