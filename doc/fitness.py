def fitness_fun(chromosome, o, r, graph, t, path):

    weight = 0
    obstacles = o[:]

    if r == t:
        score += SOLVED_AWARD

    for node in path:
        if r == node:
            score += ROBOT_ON_PATH_AWARD

    count_obs = 0
    for obstacle in obstacles:
        if obstacle in path:
            count_obs += 1
            score = score - OBSTACLE_PENALTY

    if ssolver.is_hole(o, r, t) and count_obs == 0:
        score += CLOSE_AWARD

    for move in chromosome:
        if move == ('0', '0', 0, []):
            score -= NO_MORE_STATES_PENALTY
            break
        
    for i in range(len(chromosome)):
        weight += chromosome[i][2]
    score = - weight * WEIGHT_PENALTY
        
    return score
