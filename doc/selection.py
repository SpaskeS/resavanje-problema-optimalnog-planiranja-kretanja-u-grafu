def tournament_selection(population, tournament_size):
    winner = None
    tournament = random.sample(population, tournament_size)
    
    winner = max(tournament, key = lambda item: item[0])
    
    return winner

def selection(population, reproduction_size, tournament_size):
    selected = [] 
    
    while len(selected) < reproduction_size:
        selected.append(tournament_selection(population, 
                                             tournament_size))
        
    return selected
