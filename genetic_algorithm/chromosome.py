import random

class Chromosome:
    def __init__(self, length, lower_bound, upper_bound, genes=None):
        """ Inicjalizacja chromosomu """
        self.length = length
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        if genes is None:
            self.genes = [random.choice([0, 1]) for _ in range(length)]  # Losowe bity
        else:
            self.genes = genes  # Jeśli podane, ustaw istniejące geny

        self.fitness = None  # Przystosowanie obliczane później

    def decode(self):
        """ Dekodowanie wartości binarnej do liczby rzeczywistej """
        binary_value = int("".join(map(str, self.genes)), 2)
        decimal_value = self.lower_bound + (self.upper_bound - self.lower_bound) * (binary_value / (2**self.length - 1))
        return decimal_value

    def __repr__(self):
        return f"Chromosome({self.genes}) -> Decoded: {self.decode()} | Fitness: {self.fitness}"
