from chromosome import Chromosome
from config import POPULATION_SIZE

class Population:
    def __init__(self, number_of_variables, precision, variables_list):
        """Tworzy populację chromosomów."""
        self.size = POPULATION_SIZE  # Pobieramy wartość z config.py
        self.number_of_variables = number_of_variables
        self.precision = precision
        self.variables_list = variables_list
        self.individuals = []  # Lista przechowująca osobniki

        self.initialize()

    def initialize(self):
        """Inicjalizuje populację losowymi chromosomami."""
        self.individuals = [
            Chromosome(self.number_of_variables, self.precision, self.variables_list) 
            for _ in range(self.size)
        ]
        for individual in self.individuals:
            individual.generate_chromosome()  # Tworzymy losowy chromosom

    def evaluate(self, fitness_function):
        """Ewaluacja populacji na podstawie funkcji przystosowania."""
        for individual in self.individuals:
            individual.decode_variables()  # Dekodujemy chromosom do wartości rzeczywistych
            individual.fitness = fitness_function(individual.decoded_variables)

    def get_best(self):
        """Zwraca najlepszego osobnika z populacji."""
        return max(self.individuals, key=lambda x: x.fitness)

    def get_population_size(self):
        """Zwraca liczbę osobników w populacji."""
        return len(self.individuals)
