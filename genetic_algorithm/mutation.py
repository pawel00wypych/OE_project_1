import random

class Mutation:
    @staticmethod
    def boundary(chromosome):
        """ Mutacja brzegowa - zmienia losowy gen na wartość graniczną (0 lub 1) """
        index = random.randint(0, len(chromosome.genes) - 1)
        chromosome.genes[index] = random.choice([0, 1])

    @staticmethod
    def one_point(chromosome, mutation_prob):
        """ Mutacja jednopunktowa - zmienia losowy bit z prawdopodobieństwem mutation_prob """
        for i in range(len(chromosome.genes)):
            if random.random() < mutation_prob:
                chromosome.genes[i] = 1 - chromosome.genes[i]  # Odwracamy bit

    @staticmethod
    def two_point(chromosome, mutation_prob):
        """ Mutacja dwupunktowa - zmienia dwa losowe bity z prawdopodobieństwem mutation_prob """
        indices = random.sample(range(len(chromosome.genes)), 2)  # Wybierz dwa różne miejsca
        for index in indices:
            if random.random() < mutation_prob:
                chromosome.genes[index] = 1 - chromosome.genes[index]  # Odwracamy bit
