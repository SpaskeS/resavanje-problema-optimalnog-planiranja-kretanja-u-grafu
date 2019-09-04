def crossover(parent1, parent2, o, r, graph, 
              t, population_size, path):

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
    new_o, new_r = ssolver.make_moves(obstacles, robot, 
                                      graph, new_moves)

    if len(moves1) <= len(moves2):
        for j in range(i, len(moves2)):
            if moves2[j] in ssolver.possible_moves(new_o, new_r,
                                                   graph) and
                            different_moves(moves2[j], 
                                            new_moves[-1]):
                new_moves.append(moves2[j])
                new_o, new_r = ssolver.make_move(new_o, new_r, graph,
                                                 moves2[j][0], 
                                                 moves2[j][1])
                if new_r == t:
                    break
    else:
        for j in range(0, len(moves1)):
            if moves1[j] in ssolver.possible_moves(new_o, new_r,
                                                   graph) and
                            different_moves(moves1[j],
                                            new_moves[-1]):
                new_moves.append(moves1[j])
                new_o, new_r = ssolver.make_move(new_o, new_r, graph
                                                 moves1[j][0],
                                                 moves1[j][1])
                if new_r == t:
                    break

    child = fit_chromosome(new_moves, obstacles, robot, 
                           graph, population_size, path, t)
    return child
