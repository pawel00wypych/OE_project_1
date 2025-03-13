import random
import sys

sys.path.append('../..')
from genetic_algorithm.chromosome import Chromosome
from genetic_algorithm.inversion import Inversion

def get_input(inputValue, default_value=None):
    user_input = input(inputValue)
    if user_input == "":
        return default_value
    try:
        return float(user_input)
    except ValueError:
        print("Invalid input! Please enter a number between 0 and 1.")
        return get_input(inputValue, default_value)
    
# inversion test on generated chromosome
if __name__ == "__main__":
    
    num_variables = 10
    precision = 2
    variables_list = [(0, 5), (-1, 7), (2, 8), (1,2), (1,2), (1,2), (1,2), (1,2), (1,2), (1,2)]

    chromosome = Chromosome(num_variables, precision, variables_list)
    chromosome.generate_chromosome()
    chromosome.decode_variables()
    chromosome.fitness = random.randint(1, 100)

    print("\nOriginal Chromosome:")
    print(chromosome.decoded_variables)
    chromosome_before = chromosome.decoded_variables.copy()

    inversion_probability = get_input("Enter inversion probability (0-1): ", 0.5)
    inversion_level = get_input("Enter inversion level (0-1) or press Enter for random: ", None)

    # chromosome before and after inversion
    Inversion.apply_inversion(chromosome, inversion_probability, inversion_level)
    print("\nChromosome after inversion:")
    print(chromosome.decoded_variables)

    if(chromosome.decoded_variables == chromosome_before):
        print("No inversion!")
    else:
        print("Successful inversion!")
