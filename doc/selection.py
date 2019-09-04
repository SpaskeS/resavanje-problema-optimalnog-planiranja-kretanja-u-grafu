def tournament_selection(population, tournament_size):
    pop = copy.copy(population)

    winner = None
    tournament = []
    for i in range(tournament_size):
        c = random.choice(pop)
        tournament.append(c)

    winner = max(tournament, key=lambda item:item[0])

    return winner


def selection(population, reproduction_size, tournament_size):

    pop = copy.copy(population)
    selected = []

    while len(selected) < reproduction_size:
        selected.append(tournament_selection(pop, tournament_size))

    return selected
