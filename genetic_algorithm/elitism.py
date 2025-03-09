class Elitism:
    @staticmethod
    def apply(population, new_population, elitism_count):
        """
        Zastosowanie strategii elitarnej: przeniesienie najlepszych osobników do nowej populacji.
        :param population: Stara populacja.
        :param new_population: Nowa populacja (jeszcze niepełna).
        :param elitism_count: Liczba osobników do przeniesienia.
        """
        # Sortowanie populacji według wartości przystosowania (fitness)
        best_individuals = sorted(population.individuals, key=lambda x: x.fitness, reverse=True)
        
        # Przeniesienie najlepszych osobników do nowej populacji
        for i in range(min(elitism_count, len(best_individuals))):
            new_population.append(best_individuals[i])
