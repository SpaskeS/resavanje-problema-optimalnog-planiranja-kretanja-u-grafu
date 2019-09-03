def mutation(chromosome, o, r, graph, population_size, path, t):

    moves = chromosome[1]
    obstacles = copy.deepcopy(o)
    robot = r
    new_o, new_r = ssolver.make_moves(obstacles, robot, 
                                      graph, moves)

    pm = ssolver.possible_moves(new_o, new_r, graph)

    for p in pm:
        if different_moves(p, moves[-1]):
            moves.append(p)
            break

    new_o, new_r = ssolver.make_moves(copy.deepcopy(o), r, 
                                      graph, moves)

    mutated = fit_chromosome(moves, copy.deepcopy(o), r, graph, 
                             population_size, path, t)

    return mutated
