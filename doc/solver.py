def solve_genetic(o, r, graph, t, path):

    chromosome_size = len(path) * obstacles_in_path

    population_size = 100
    elite_size = 60
    max_iterations = 200
    reproduction_size = 30
    tournament_size = 10

    initial_population = create_initial_population(o, r, graph, t,
                                                   chromosome_size, 
                                                   POPULATION_SIZE)

    scored_population = []
    for i in range(population_size):
        chromosome = initial_population[i]
        scored_population.append(fit_chromosome(chromosome, o, r, 
                                                graph, 
                                                POPULATION_SIZE, 
                                                path, t))

    current_pop = copy.copy(scored_population)

    for i in range(max_iterations):

        elite = []
        for_selection = copy.copy(current_pop)
        for j in range(elite_size):
            largest = max(for_selection, key=lambda item:item[0])
            elite.append(largest)
            for_selection.remove(largest)

        selected = selection(for_selection, 
                             reproduction_size, 
                             tournament_size)
        current_pop = create_new_generation(elite, selected,
                                            population_size, 
                                            elite_size, o, r, 
                                            graph, t, path)

        best = max(current_pop, key=lambda item:item[0])

    return best[1]
