import random

class Inversion:
    @staticmethod
    def invert(chromosome, inversion_prob):
        """
        Operator inwersji: odwraca losowy fragment chromosomu.
        :param chromosome: Chromosom, który podlega inwersji.
        :param inversion_prob: Prawdopodobieństwo inwersji.
        """
        if random.random() < inversion_prob:
            # Wybór dwóch losowych punktów
            point1 = random.randint(0, len(chromosome.genes) - 2)
            point2 = random.randint(point1 + 1, len(chromosome.genes) - 1)
            # Odwrócenie fragmentu
            chromosome.genes[point1:point2] = reversed(chromosome.genes[point1:point2])
