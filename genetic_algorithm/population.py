from genetic_algorithm.chromosome import Chromosome

class Population:
    def __init__(self, number_of_variables, precision, variables_ranges_list, individuals=None, population_size = 100):
        """Create population of individuals."""
        self.size = population_size
        self.number_of_variables = number_of_variables
        self.precision = precision
        self.variables_ranges_list = variables_ranges_list
        if individuals is None:
            self.individuals = []
        else:
            self.individuals = individuals
        self.initialize()

    def initialize(self):
        """Initiate population with random chromosomes/individuals."""
        self.individuals = [
            Chromosome(self.number_of_variables, self.precision, self.variables_ranges_list)
            for _ in range(self.size)
        ]
        for individual in self.individuals:
            individual.generate_chromosome()

    def evaluate(self, fitness_function):
        """Evaluate population using given fitness function"""
        for individual in self.individuals:
            individual.decode_variables()
            individual.fitness = fitness_function(individual.decoded_variables)

    def get_population_size(self):
        """Return size of the population."""
        return len(self.individuals)
