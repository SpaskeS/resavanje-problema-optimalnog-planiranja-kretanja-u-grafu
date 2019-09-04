def fitness_fun(chromosome, o, r, graph, t, path):
        
    weight = 0
    obstacles = copy.copy(o)
    for i in range(len(chromosome)):
        weight += chromosome[i][2]

    score = - weight

    if r == t:
        score += SOLVED_AWARD

    for node in path:
        if node == r:
            distance = nx.shortest_path_length(graph, r, t)
            for obstacle in obstacles:
                if obstacle in path:
                    distance -= 1
            score += LENGTH_FACTOR*((len(path)-distance+1))

    count_obs = 0
    for obstacle in obstacles:
        if obstacle in path:
            count_obs += 1
            obs_distance = nx.shortest_path_length(graph, 
                                                   obstacle, t)
            score = score - OBS_DIST_PENALTY*count_obs - 
                    OBS_DIST*(len(path)-obs_distance+1)

    if ssolver.is_hole(obstacles, r, t) and count_obs == 0:
        for i in range(0, len(path)-1):
            for move in chromosome:
                if move == (path[i], path[i+1]) and move[0] == r:
                    score += ROBOT_MOVE_AWARD
        distance = nx.shortest_path_length(graph, r, t)
        score += R_DIST*(len(path)-distance+1)

    return score
