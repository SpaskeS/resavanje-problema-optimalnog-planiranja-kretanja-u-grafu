def create_new_generation(population, selected, population_size, 
                          elite_size, o, r, graph, t, path):
    new_generation = sorted(population, key = lambda item : item[0],
                            reverse = True)[:elite_size]
    
    while len(new_generation)  < population_size:
        parent1, parent2 = random.sample(selected, 2)
        child1, child2 = crossover(parent1, parent2, o, r, graph, t, 
                                   population_size, path)
        
        new_generation.append(child1)
        new_generation.append(child2)
        
    return new_generation
