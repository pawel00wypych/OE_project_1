import random

class  Mutation:
    def __init__(self,
                 population,
                 mutation_probability=0.15):
        self.population = population                        # Population without elite individuals!
        self.mutation_probability = mutation_probability    # By default 15%

    def single_point_mutation(self):
        for individual in self.population:
            bit_start_indx = 0
            for j in range(individual.number_of_variables):
                bit_range = individual.number_of_bits_variables[j]
                if self.decide_to_mutate() and bit_range > 0:
                    m_bit = random.randint(bit_start_indx,
                                           bit_start_indx + bit_range - 1)
                    individual.chromosome[m_bit] = 1 - individual.chromosome[m_bit]
                bit_start_indx += bit_range
        return self.population

    def two_point_mutation(self):
        for individual in self.population:
            bit_start_indx = 0
            for j in range(individual.number_of_variables):
                bit_range = individual.number_of_bits_variables[j]
                if self.decide_to_mutate() and bit_range > 1:
                    m_bit_1, m_bit_2 = sorted(random.sample(range(bit_start_indx,
                                                                  bit_start_indx + bit_range - 1),
                                                            2))
                    individual.chromosome[m_bit_1] = 1 - individual.chromosome[m_bit_1]
                    individual.chromosome[m_bit_2] = 1 - individual.chromosome[m_bit_2]
                bit_start_indx += bit_range
        return self.population

    def edge_mutation(self):
        for individual in self.population:
            bit_start_indx = 0
            for j in range(individual.number_of_variables):
                bit_range = individual.number_of_bits_variables[j]
                if self.decide_to_mutate() and bit_range > 0:
                    if random.randint(0,1) >= 0.5:
                        m_bit = bit_start_indx
                    else:
                        m_bit = bit_start_indx + bit_range - 1
                    individual.chromosome[m_bit] = 1 - individual.chromosome[m_bit]
                bit_start_indx += bit_range
        return self.population

    def decide_to_mutate(self):
        return random.random() < self.mutation_probability