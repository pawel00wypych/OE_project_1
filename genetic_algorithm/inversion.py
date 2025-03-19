import random

class Inversion:
    @staticmethod
    def apply_inversion(chromosome, inversion_probability, inversion_level=None):
        # inversion with a probability and level parameters to config its chance and size
        # if inversion level is none, its randomly chosen
        if inversion_level is None:
            inversion_level = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

        if random.random() <= inversion_probability:
            # length of inversion based on inversion level
            chromosome_length = chromosome.number_of_bits_chromosome
            inversion_length = int(chromosome_length * inversion_level)
            # randomly choosing chromose frragment to inverse
            start_index = random.randint(0, chromosome_length - inversion_length)
            end_index = start_index + inversion_length - 1
            # inversion
            chromosome.decoded_variables[start_index:end_index] = reversed(chromosome.decoded_variables[start_index:end_index])
