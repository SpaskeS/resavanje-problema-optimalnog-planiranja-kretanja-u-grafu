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
