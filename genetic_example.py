 def selection(self, chromosomes):
        selected = []

        # Bira se self.reproduction_size hromozoma za reprodukciju
        # Selekcija moze biti ruletska ili turnirska
        for i in range(self.reproduction_size):
            if self.selection_type == 'roulette':
                selected.append(self.roulette_selection(chromosomes))
            elif self.selection_type == 'tournament':
                selected.append(self.tournament_selection(chromosomes))

        # Vracaju se izabrani hromozomi za repodukciju
        return selected




'''Bira jednu jedinku koristeci turnirsku selekciju. '''
  def tournament_selection(self, chromosomes):

      # bira se  self.tournament_size jediniki za turnir
      selected = random.sample(chromosomes, self.tournament_size)

      # pobednik je onaj sa najboljom prilagodjenosti
      winner = max(selected, key = lambda x: x.fitness)

      return winner

  '''Vrsi mutaciju nad hromozomom sa verovatnocom self._mutation_rate.
     Mutacija se vrsi nad jednim genom (karakterom) sa proizvoljnim indeksom.
  '''
  def mutate(self, genetic_code):
      random_value = random.random()

      # ukoliko je ispunjen uslov, izvrsi mutaciju
      if random_value < self.mutation_rate:

          # izabrati proizvoljan indeks
          random_index = random.randrange(self.chromosome_size)

          while True:
              # izabrati novu proizvoljnu vrednost za karakter
              new_value = random.choice(self.possible_gene_values)

              # ukoliko su vrednosti razlicite, izmeni karakter
              if genetic_code[random_index] != new_value:
                  break

          genetic_code[random_index] = new_value

      return genetic_code

  '''Od jedinki generise novu generaciju primenjujuci genetske operatore
     ukrstanje (crossover) i mutaciju (mutation).
  '''
  def create_generation(self, chromosomes):
      generation = []
      generation_size = 0

      while generation_size < self.generation_size:
          # Proizvoljno se biraju 2 roditelja za ukrstanje
          [parent1, parent2] = random.sample(chromosomes, 2)

          # Dobijaju se 2 detata ukrstanjem
          child1_code, child2_code = self.crossover(parent1, parent2)

          # Vrsi se mutacija nad decom
          child1_code = self.mutate(child1_code)
          child2_code = self.mutate(child2_code)

          # Prave se novi hromozomi
          child1 = Chromosome(child1_code, self.calculate_fitness(child1_code))
          child2 = Chromosome(child2_code, self.calculate_fitness(child2_code))

          # Dodaju se u generaciju
          generation.append(child1)
          generation.append(child2)

          generation_size += 2

      return generation

  '''Jednopoziciono ukrstanje sa nasumicnom tackom ukrstanja'''
  def crossover(self, parent1, parent2):

      # bira se proizvoljna tacka ukrstanja
      break_point = random.randrange(1, self.chromosome_size)

      child1 = parent1.genetic_code[:break_point] + parent2.genetic_code[break_point:]
      child2 = parent2.genetic_code[:break_point] + parent1.genetic_code[break_point:]

      return (child1, child2)

  '''Izvrsavanje genetskog algoritma'''
  def optimize(self):
      # Generisi pocetnu populaciju jedinki i izracunaj
      # prilagodjenost svake jedinke u populaciji
      population = self.initial_population()

      for i in range(0, self.max_iterations):
          # Selekcija (ruletska ili turnirska)
          selected = self.selection(population)

          # Kreiraj generaciju ukrstanjem i mutacijom
          population = self.create_generation(selected)

          # Najkvalitetnija jedinka
          global_best_chromosome = max(population, key=lambda x: x.fitness)

          print(global_best_chromosome)

          if global_best_chromosome.fitness == self.chromosome_size:
              break

      return global_best_chromosome
