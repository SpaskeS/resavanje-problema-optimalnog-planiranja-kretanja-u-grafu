def create_new_generation(elite, selected, population_size, elite_size, o, r, graph, t, path):

    new_generation = copy.copy(elite)

    random_elite = random.choice(new_generation)
    while len(new_generation) < population_size:

        valid_parents = False
        while(valid_parents == False):
            parent1, parent2 = random.sample(selected, 2)

            if len(parent1[1]) > P_LENGTH and
               len(parent2[1]) > P_LENGTH:
                child1 = crossover(parent1, parent2, o, r, graph,
                                   t, population_size, path)
                valid_parents = True


        if random.randrange(0, 100) < MUTATION_RATE:
            mutated_elite = mutation(random_elite, o, r, graph, 
                                     population_size, path, t)
            mutated_child = mutation(child1, o, r, graph,
                                     population_size, path, t)
            new_generation.append(mutated_child)
            new_generation.append(mutated_elite)
        else:
            new_generation.append(child1)

    return new_generation
