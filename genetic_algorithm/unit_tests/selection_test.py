import random
import sys

sys.path.append('../..')
from genetic_algorithm.selection import Selection

class Individual:
    def __init__(self, fitness):
        self.fitness = fitness

class Population:
    def __init__(self, individuals):
        self.individuals = individuals

# selection test on defualt population and individuals
if __name__ == "__main__":
    population_size = 10
    individuals = [Individual(fitness=random.randint(1, 100)) for _ in range(population_size)]
    population = Population(individuals)

    # printing the individuals in the population
    print("\nPopulation:")
    for individual in population.individuals:
        print(individual.fitness)

    # Testing best selection
    print("\nBest Selection:")
    best_individuals = Selection.best_selection(population, num_selected=3)
    for ind in best_individuals:
        print(f"Fitness: {ind.fitness}")

    # Testing roulette selection
    print("\nRoulette Selection:")
    selected_by_roulette = Selection.roulette_selection(population, num_selected=3)
    for ind in selected_by_roulette:
        print(f"Fitness: {ind.fitness}")

    # Testing tournament selection
    print("\nTournament Selection:")
    selected_by_tournament = Selection.tournament_selection(population, num_selected=3, tournament_size=4)
    for ind in selected_by_tournament:
        print(f"Fitness: {ind.fitness}")