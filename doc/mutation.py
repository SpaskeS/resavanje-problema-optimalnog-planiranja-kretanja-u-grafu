def mutation(chromosome, o, r, graph, population_size, path, t):

    moves = chromosome[1]

    obstacles = copy.copy(o)
    robot = r
    new_o, new_r = ssolver.make_moves(obstacles, robot,
                                      graph, moves)
    if new_r == t:
        return chromosome

    pm = ssolver.possible_moves(new_o, new_r, graph)

    for p in pm:
        if p[0] == new_r and different_moves(p, moves[-1]):
            moves.append(p)
            break
        elif different_moves(p, moves[-1]):
            moves.append(p)
            break

    new_o, new_r = ssolver.make_moves(copy.copy(o), r, graph, moves)
    mutated = fit_chromosome(moves, copy.copy(o), r, graph, 
                             population_size, path, t)

    return mutated
