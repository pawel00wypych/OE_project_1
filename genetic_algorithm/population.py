from genetic_algorithm.chromosome import Chromosome
from genetic_algorithm.config import POPULATION_SIZE

class Population:
    def __init__(self, number_of_variables, precision, variables_ranges_list, individuals):
        """Tworzy populację chromosomów."""
        self.size = POPULATION_SIZE  # Pobieramy wartość z config.py
        self.number_of_variables = number_of_variables
        self.precision = precision
        self.variables_ranges_list = variables_ranges_list
        if individuals is None:
            self.individuals = []  # Lista przechowująca osobniki
        else:
            self.individuals = individuals
        self.initialize()

    def initialize(self):
        """Inicjalizuje populację losowymi chromosomami."""
        self.individuals = [
            Chromosome(self.number_of_variables, self.precision, self.variables_ranges_list)
            for _ in range(self.size)
        ]
        for individual in self.individuals:
            individual.generate_chromosome()  # Tworzymy losowy chromosom

    def evaluate(self, fitness_function):
        """Ewaluacja populacji na podstawie funkcji przystosowania."""
        for individual in self.individuals:
            individual.decode_variables()  # Dekodujemy chromosom do wartości rzeczywistych
            individual.fitness = fitness_function(individual.decoded_variables)

    def get_population_size(self):
        """Zwraca liczbę osobników w populacji."""
        return len(self.individuals)
