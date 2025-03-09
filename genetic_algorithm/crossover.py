import random

class Crossover:
    @staticmethod
    def one_point(parent1, parent2):
        """ Krzyżowanie jednopunktowe """
        point = random.randint(1, len(parent1.genes) - 1)
        child1_genes = parent1.genes[:point] + parent2.genes[point:]
        child2_genes = parent2.genes[:point] + parent1.genes[point:]
        return child1_genes, child2_genes

    @staticmethod
    def two_point(parent1, parent2):
        """ Krzyżowanie dwupunktowe """
        point1 = random.randint(1, len(parent1.genes) - 2)
        point2 = random.randint(point1 + 1, len(parent1.genes) - 1)
        child1_genes = (
            parent1.genes[:point1] + parent2.genes[point1:point2] + parent1.genes[point2:]
        )
        child2_genes = (
            parent2.genes[:point1] + parent1.genes[point1:point2] + parent2.genes[point2:]
        )
        return child1_genes, child2_genes

    @staticmethod
    def uniform(parent1, parent2):
        """ Krzyżowanie jednorodne """
        child1_genes = []
        child2_genes = []
        for i in range(len(parent1.genes)):
            if random.random() < 0.5:
                child1_genes.append(parent1.genes[i])
                child2_genes.append(parent2.genes[i])
            else:
                child1_genes.append(parent2.genes[i])
                child2_genes.append(parent1.genes[i])
        return child1_genes, child2_genes

    @staticmethod
    def granular(parent1, parent2, granularity=0.3):
        """ Krzyżowanie ziarniste - losowe przełączanie fragmentów """
        child1_genes = parent1.genes[:]
        child2_genes = parent2.genes[:]
        for i in range(len(parent1.genes)):
            if random.random() < granularity:
                child1_genes[i], child2_genes[i] = child2_genes[i], child1_genes[i]
        return child1_genes, child2_genes
