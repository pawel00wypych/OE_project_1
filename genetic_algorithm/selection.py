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
        
        # minimal and maximal fitness to define a scaled probabilities
        min_fitness = min(individual.fitness for individual in available_individuals)
        max_fitness = max(individual.fitness for individual in available_individuals)

        # identical fitness case
        if max_fitness == min_fitness:
            selected_individuals = random.sample(available_individuals, num_selected)
            return selected_individuals

        # minimal offset to give worst fitness value a chance to be picked 
        min_offset = 0.01
        # scaled fitness
        for individual in available_individuals:
            scaled_fitness = ((individual.fitness - min_fitness) / (max_fitness - min_fitness)) + min_offset
            individual.scaled_fitness = scaled_fitness

        total_scaled_fitness = sum(individual.scaled_fitness for individual in available_individuals)

        # chosen individuals 
        chosen = set()

        for _ in range(num_selected):
            pick = random.uniform(0, total_scaled_fitness)
            current = 0

            for individual in available_individuals:
                # skipping chosen individuals
                if individual in chosen:
                    continue

                current += individual.scaled_fitness

                if current > pick:
                    selected_individuals.append(individual)
                    chosen.add(individual)
                    total_scaled_fitness -= individual.scaled_fitness
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