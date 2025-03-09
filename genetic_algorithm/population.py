from chromosome import Chromosome

class Population:
    def __init__(self, size, chromosome_length, lower_bound, upper_bound):
        """
        Tworzy populację chromosomów.
        :param size: Liczba osobników w populacji.
        :param chromosome_length: Długość chromosomu w bitach.
        :param lower_bound: Dolna granica wartości zmiennych.
        :param upper_bound: Górna granica wartości zmiennych.
        """
        self.size = size
        self.chromosome_length = chromosome_length
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.individuals = [Chromosome(chromosome_length, lower_bound, upper_bound) for _ in range(size)]

    def evaluate(self, fitness_function):
        """
        Ocena populacji na podstawie funkcji przystosowania.
        """
        for individual in self.individuals:
            individual.fitness = fitness_function(individual.decode())

    def get_best(self):
        """
        Zwraca najlepszego osobnika w populacji.
        """
        return max(self.individuals, key=lambda x: x.fitness)

    def __repr__(self):
        return "\n".join([str(ind) for ind in self.individuals])
