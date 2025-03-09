import random

class Selection:
    @staticmethod
    def best_selection(population, num_selected):
        """
        Selekcja najlepszych osobników (elitarnych).
        :param population: Populacja osobników.
        :param num_selected: Liczba osobników do wybrania.
        :return: Lista wybranych osobników.
        """
        sorted_population = sorted(population.individuals, key=lambda x: x.fitness, reverse=True)
        return sorted_population[:num_selected]

    @staticmethod
    def roulette_selection(population):
        """
        Selekcja ruletkowa (koło ruletki).
        :param population: Populacja osobników.
        :return: Wybrany osobnik.
        """
        total_fitness = sum(ind.fitness for ind in population.individuals)
        pick = random.uniform(0, total_fitness)
        current = 0
        for ind in population.individuals:
            current += ind.fitness
            if current > pick:
                return ind

    @staticmethod
    def tournament_selection(population, tournament_size):
        """
        Selekcja turniejowa.
        :param population: Populacja osobników.
        :param tournament_size: Liczba osobników w turnieju.
        :return: Najlepszy osobnik z turnieju.
        """
        tournament = random.sample(population.individuals, tournament_size)
        return max(tournament, key=lambda x: x.fitness)
