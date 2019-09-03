def create_new_generation(population, selected, population_size, 
                          elite_size, o, r, graph, t, path):
    new_generation = sorted(population, key = lambda item : item[0],
                            reverse = True)[:elite_size]
    
    while len(new_generation)  < population_size:
        
        valid_parents = False
        while(valid_parents == False):
            parent1, parent2 = random.sample(selected, 2)
            
            if len(parent1[1]) > MIN_PARENT_LEN and
               len(parent2[1]) > MIN_PARENT_LEN:
                    
                child = crossover(parent1, parent2, o, r, graph,
                                  t, population_size, path)
                valid_parents = True
        
        if random.randrange(0, 100) < MUTATION_RATE:
            mutated_child = mutation(child, o, r, graph,
                                     population_size, path, t)
            new_generation.append(mutated_child)
        else:
            new_generation.append(child)
        
    return new_generation
