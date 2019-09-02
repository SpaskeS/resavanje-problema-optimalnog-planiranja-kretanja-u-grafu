def solve_genetic(o, r, graph, t, path):
    
    chromosome_size = len(path) * OBSTACLES_IN_PATH
    
    inital_population = create_initial_population(o, r, graph, t
                                                  chromosome_size,
                                                  POPULATION_SIZE)
    
    scored_population = []
    for i in range(POPULATION_SIZE):
        chromosome = inital_population[i]
        scored_population.append(fit_chromosome(chromosome, o,
                                                r, graph,
                                                population_size,
                                                path, t))
        
    
    current_pop = scored_population[:]
    
    for i in range(MAX_ITERATIONS):
        selected = selection(current_pop, REPRODUCTION_SIZE,
                             TOURNAMENT_SIZE)
        current_pop = create_new_generation(current_pop, selected, 
                                            population_size, e
                                            lite_size, o, r, 
                                            graph, t, path)
        
        best = max(current_pop, key = lambda item:item[0])
        if best >= GOOD_ENOUGH:
            break
        

    return best[1]
