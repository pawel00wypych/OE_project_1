import random
import heapq

class Selection:
    # best selection - selection method to choose the best individals
    @staticmethod
    def best_selection(population, num_selected):
        # sorting individuals in population by fitness, returning num_selected best individuals from the list
        selected_individuals = heapq.nlargest(num_selected, population.individuals, key=lambda individual: individual.fitness)

        return sorted(selected_individuals, key=lambda individual: individual.fitness, reverse=True)

    # roulette selection - selection method to choose randomly
    # but better individuals has better chances
    @staticmethod
    def roulette_selection(population, num_selected):
        # randomly choosing individuals num_selected times, fitness score decide thier probability to be picked
        selected_individuals = []
        available_individuals = population.individuals[:]
        total_fitness = sum(individual.fitness for individual in population.individuals)

        for _ in range(num_selected):
            pick = random.uniform(0, total_fitness)
            current = 0

            for individual in available_individuals:
                current += individual.fitness

                if current > pick:
                    selected_individuals.append(individual)
                    available_individuals.remove(individual)
                    total_fitness -= individual.fitness
                    break

        return sorted(selected_individuals, key=lambda individual: individual.fitness, reverse=True)

    # tournaments selection - selection method to choose the best individals
    # from defined groups
    @staticmethod
    def tournament_selection(population, num_selected, tournament_size):
        # creating a num_selected number of tournaments by random samples based on tournament size
        # choosing the best individuals from tournaments
        available_individuals = population.individuals[:]
        random.shuffle(available_individuals)
        selected_individuals = []

        if tournament_size > len(population.individuals):
            tournament_size = len(population.individuals)

        tournaments = [available_individuals[i:i + tournament_size] for i in range(0, len(available_individuals), tournament_size)]

        # skipping empty tournaments
        for tournament in tournaments:
            if not tournament:
                continue  

            winner = max(tournament, key=lambda individual: individual.fitness)
            selected_individuals.append(winner)

            if len(selected_individuals) >= num_selected:
                break

        return sorted(selected_individuals, key=lambda individual: individual.fitness, reverse=True)