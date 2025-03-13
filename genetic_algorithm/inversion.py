import random

def inversion(chromosome, inversion_probability, inversion_level=None):
    # inversion with a probability and level parameters to config its chance and size
    # if inversion level is none, its randomly chosen
    if inversion_level is None:
        inversion_level = random.choice([0.1, 0.2, 0.3, 0.4, 0.5])

    if random.random() <= inversion_probability:
        # length of inversion based on inversion level
        inversion_length = int(len(chromosome) * inversion_level)
        # randomly choosing chromose frragment to inverse
        start_index = random.randint(0, len(chromosome) - inversion_length)
        end_index = start_index + inversion_length
        # inversion
        chromosome[start_index:end_index] = reversed(chromosome[start_index:end_index])