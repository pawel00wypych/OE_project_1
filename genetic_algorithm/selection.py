import random
import heapq

class Selection:
    # best selection - selection method to choose the best individals
    @staticmethod
    def best_selection(population, num_selected):
        # sorting individuals in population by fitness, returning num_selected best individuals from the list
        selected_individuals = heapq.nlargest(num_selected, population.individuals, key=lambda individual: individual.fitness)
        return selected_individuals

    # roulette selection - selection method to choose randomly
    # but better individuals has better chances
    @staticmethod
    def roulette_selection(population, num_selected):
        # randomly choosing individuals num_selected times, fitness score decide thier probability to be picked
        selected_individuals = []
        total_fitness = sum(individual.fitness for individual in population.individuals)

        for _ in range(num_selected):
            pick = random.uniform(0, total_fitness)
            current = 0
            for individual in population.individuals:
                current += individual.fitness
                if current > pick:
                    selected_individuals.append(individual)
                    break
        return selected_individuals

    # tournaments selection - selection method to choose the best individals
    # from defined groups
    @staticmethod
    def tournament_selection(population, num_selected, tournament_size):
        # creating a num_selected number of tournaments by random samples based on tournament size
        # choosing the best individuals from tournaments
        selected_individuals = []
        if tournament_size > len(population.individuals):
            tournament_size = len(population.individuals)

        for _ in range(num_selected):
            tournament = random.sample(population.individuals, tournament_size)
            selected_individuals.append(max(tournament, key=lambda individual: individual.fitness))
        return selected_individuals