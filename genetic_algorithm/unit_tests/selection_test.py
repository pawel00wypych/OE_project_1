import random
import sys

sys.path.append('../')
from genetic_algorithm.chromosome import Chromosome
from genetic_algorithm.selection import Selection

class Population:
    def __init__(self, individuals):
        self.individuals = individuals 

# selection test on defualt population and individuals
if __name__ == "__main__":
    population_size = 10
    num_variables = 3
    precision = 2
    variables_list = [(0, 5), (-1, 7), (2, 8)]

    individuals = []
    for _ in range(population_size):
        chromosome = Chromosome(num_variables, precision, variables_list)
        chromosome.generate_chromosome()
        chromosome.decode_variables()
        chromosome.fitness = random.randint(1, 100)
        individuals.append(chromosome)
    
    population = Population(individuals)

    # printing the individuals in the population
    print("\nPopulation:")
    for individual in population.individuals:
        print(individual.fitness)

    # Testing best selection
    print("\nBest Selection:")
    best_individuals = Selection.best_selection(population, num_selected=3)
    for individual in best_individuals:
        print(f"Fitness: {individual.fitness}, Decoded: {individual.decoded_variables}")

    # Testing roulette selection
    print("\nRoulette Selection:")
    selected_by_roulette = Selection.roulette_selection(population, num_selected=3)
    for individual in selected_by_roulette:
        print(f"Fitness: {individual.fitness}, Decoded: {individual.decoded_variables}")

    # Testing tournament selection
    print("\nTournament Selection:")
    selected_by_tournament = Selection.tournament_selection(population, num_selected=3)
    for individual in selected_by_tournament:
        print(f"Fitness: {individual.fitness}, Decoded: {individual.decoded_variables}")