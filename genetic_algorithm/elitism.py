
class Elitism:
    def __init__(self,
                 population=None
                 ):
        if population is None:
            population = []
        self.population = population
        self.elite_individuals = []
        self.best_fitness_val = 0
        self.number_of_elites = self.configure_num_of_elite()

    def choose_the_best_individuals(self):
        sorted_population = sorted(self.population,
                                    key=lambda individual: individual.fitness,
                                    reverse=True)
        self.best_fitness_val = sorted_population[0].fitness
        self.elite_individuals = sorted_population[:self.number_of_elites]

    def configure_num_of_elite(self):
        pop_size = len(self.population)
        if pop_size <= 20:
            return 1
        elif pop_size <= 100:
            return  pop_size // 20
        else:
            return pop_size // 15

    def set_new_population(self,
                           population):
        if len(population) > 0:
            self.population = population

    def get_elite_list(self):
        return self.elite_individuals