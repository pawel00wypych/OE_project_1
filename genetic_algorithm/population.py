from chromosome import Chromosome

class Population:
    def __init__(self, size, chromosome_length, lower_bound, upper_bound):
        """Tworzy populację chromosomów."""
        self.size = size
        self.chromosome_length = chromosome_length
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.individuals = [Chromosome(chromosome_length, lower_bound, upper_bound) for _ in range(size)]

    def evaluate(self, fitness_function):
        """Ewaluacja populacji na podstawie funkcji przystosowania."""
        for individual in self.individuals:
            result = fitness_function([individual.decode()])

            if result is None:
                print(f"⚠️ UWAGA: Fitness zwrócił None dla {individual.decode()}!")
                result = float('-inf')  # Domyślna wartość, jeśli fitness_function zwróci None

            individual.fitness = result

    def get_best(self):
        """Zwraca najlepszego osobnika z populacji, ignorując None."""
        valid_individuals = [ind for ind in self.individuals if ind.fitness is not None]

        if not valid_individuals:
            raise ValueError("Brak poprawnych osobników w populacji - wszystkie fitnessy są None.")

        return max(valid_individuals, key=lambda x: x.fitness)
