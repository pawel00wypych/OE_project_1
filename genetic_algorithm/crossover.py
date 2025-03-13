import random
import chromosome

class  Crossover:
    def __init__(self, population,crossover_probability):
        self.population = population
        self.crossover_probability = crossover_probability

    def single_point_crossover(self):
        new_population = []
        for i in range(len(self.population) // 2):
            chromo1, chromo2 = random.sample(self.population, 2)
            if self.decide_to_crossover():
                crossover_point = random.randint(1,chromo1.number_of_bits_chromosome)
                new_chromo1, new_chromo2 = self.cross_chromosomes(chromo1,
                                                                  chromo2,
                                                                  crossover_point)
                new_population.append(new_chromo1)
                new_population.append(new_chromo2)
            else:
                new_population.append(chromo1)
                new_population.append(chromo2)
        return new_population


    def two_point_crossover(self):
        new_population = []
        for i in range(len(self.population) // 2):
            chromo1, chromo2 = random.sample(self.population,2)
            if self.decide_to_crossover():
                point1, point2 = sorted(random.sample(range(1, chromo1.number_of_bits_chromosome), 2))
                new_chromo1, new_chromo2   = self.cross_chromosomes(chromo1,
                                                                    chromo2,
                                                                    point1)
                new_chromo1, new_chromo2   = self.cross_chromosomes(new_chromo1,
                                                                    new_chromo2,
                                                                    point2)
                new_population.append(new_chromo1)
                new_population.append(new_chromo2)
            else:
                new_population.append(chromo1)
                new_population.append(chromo2)
        return new_population

    def uniform_crossover(self):
        new_population = []
        for i in range(len(self.population) // 2):
            chromo1, chromo2 = random.sample(self.population, 2)
            if self.decide_to_crossover():
                new_genes1 = [None] * chromo1.number_of_bits_chromosome
                new_genes2 = [None] * chromo2.number_of_bits_chromosome
                for j in range(chromo1.number_of_bits_chromosome):
                    if random.random() <= 0.5:
                        new_genes1[j] = chromo1.chromosome[j]
                        new_genes2[j] = chromo2.chromosome[j]
                    else:
                        new_genes1[j] = chromo2.chromosome[j]
                        new_genes2[j] = chromo1.chromosome[j]

                new_chromosome_1, new_chromosome_2 = self.create_new_chromosomes(chromo1,
                                                                                 chromo2,
                                                                                 new_genes1,
                                                                                 new_genes2)
                new_population.append(new_chromosome_1)
                new_population.append(new_chromosome_2)
            else:
                new_population.append(chromo1)
                new_population.append(chromo2)
        return new_population

    def granular_crossover(self):
        new_population = []
        for i in range(len(self.population) // 2):
            chromo1, chromo2 = random.sample(self.population, 2)
            if self.decide_to_crossover():
                new_genes1 = []
                new_genes2 = []
                bits_left = chromo1.number_of_bits_chromosome
                granule_start_point = 0
                n = 0
                while bits_left > 0:
                    granule_size = random.randint(1, chromo1.number_of_bits_chromosome // 10)
                    if (bits_left - granule_size) < 0:
                        granule_size = bits_left
                        bits_left = 0
                    else:
                        bits_left = bits_left - granule_size

                    if n%2 == 0:
                        new_genes1.extend(chromo2.chromosome[granule_start_point:granule_size])
                        new_genes2.extend(chromo1.chromosome[granule_start_point:granule_size])
                    else:
                        new_genes1.extend(chromo1.chromosome[granule_start_point:granule_size])
                        new_genes2.extend(chromo2.chromosome[granule_start_point:granule_size])

                    granule_start_point = granule_start_point + granule_size
                    n += 1
                new_chromosome_1, new_chromosome_2 = self.create_new_chromosomes(chromo1,
                                                                                 chromo2,
                                                                                 new_genes1,
                                                                                 new_genes2)
                new_population.append(new_chromosome_1)
                new_population.append(new_chromosome_2)
            else:
                new_population.append(chromo1)
                new_population.append(chromo2)
        return new_population







    def decide_to_crossover(self):
        return random.random() < self.crossover_probability

    def cross_chromosomes(self,
                          chromo1,
                          chromo2,
                          crossover_point):
        new_chromo1 = chromosome.Chromosome(chromo1.number_of_variables,
                                            chromo1.precision,
                                            chromo1.variables_list,
                                            chromo1.chromosome[:crossover_point]
                                            + chromo2.chromosome[crossover_point:])
        new_chromo2 = chromosome.Chromosome(chromo2.number_of_variables,
                                            chromo2.precision,
                                            chromo2.variables_list,
                                            chromo2.chromosome[:crossover_point]
                                            + chromo1.chromosome[crossover_point:])
        return new_chromo1, new_chromo2

    def create_new_chromosomes(self,
                               chromo1,
                               chromo2,
                               new_genes1,
                               new_genes2):
        new_chromosome1 = chromosome.Chromosome(chromo1.number_of_variables,
                                            chromo1.precision,
                                            chromo1.variables_list,
                                            new_genes1)
        new_chromosome2 = chromosome.Chromosome(chromo2.number_of_variables,
                                            chromo2.precision,
                                            chromo2.variables_list,
                                            new_genes2)
        return new_chromosome1, new_chromosome2