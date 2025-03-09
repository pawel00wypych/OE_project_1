import numpy as np
import random
from config import (
    POPULATION_SIZE, CHROMOSOME_LENGTH, NUM_GENERATIONS, LOWER_BOUND, UPPER_BOUND,
    SELECTION_METHOD, CROSSOVER_METHOD, CROSSOVER_PROB, MUTATION_METHOD, MUTATION_PROB, 
    INVERSION_PROB, ELITISM_COUNT, TEST_FUNCTION
)
from population import Population
from selection import Selection
from crossover import Crossover
from mutation import Mutation
from inversion import Inversion
from elitism import Elitism
from chromosome import Chromosome
from functions import TestFunctions

# Mapowanie nazw funkcji testowych na ich implementacje
function_map = {
    "rastrigin": TestFunctions.rastrigin,
    "sphere": TestFunctions.sphere,
    "ackley": TestFunctions.ackley,
    "schwefel": TestFunctions.schwefel,
    "rosenbrock": TestFunctions.rosenbrock
}

def run_genetic_algorithm():
    """Uruchomienie algorytmu genetycznego i zwrócenie wyników dla GUI"""
    population = Population(POPULATION_SIZE, CHROMOSOME_LENGTH, LOWER_BOUND, UPPER_BOUND)
    fitness_function = function_map.get(TEST_FUNCTION, TestFunctions.rastrigin)

    best_values = []  # Lista do przechowywania najlepszych wartości funkcji celu

    for generation in range(NUM_GENERATIONS):
        # Ewaluacja populacji
        population.evaluate(fitness_function)

        # Wybór osobników do krzyżowania zgodnie z metodą selekcji
        if SELECTION_METHOD == "best":
            selected_individuals = Selection.best_selection(population, POPULATION_SIZE // 2)
        elif SELECTION_METHOD == "roulette":
            selected_individuals = [Selection.roulette_selection(population) for _ in range(POPULATION_SIZE // 2)]
        elif SELECTION_METHOD == "tournament":
            selected_individuals = [Selection.tournament_selection(population, tournament_size=3) for _ in range(POPULATION_SIZE // 2)]
        else:
            raise ValueError("Nieznana metoda selekcji!")

        # Tworzenie nowej populacji przez krzyżowanie
        new_population = []

        # **Strategia elitarna** – przenosimy najlepszych osobników do nowej populacji
        Elitism.apply(population, new_population, ELITISM_COUNT)

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(selected_individuals, 2)

            # Wybór metody krzyżowania
            if random.random() < CROSSOVER_PROB:
                if CROSSOVER_METHOD == "one_point":
                    child1_genes, child2_genes = Crossover.one_point(parent1, parent2)
                elif CROSSOVER_METHOD == "two_point":
                    child1_genes, child2_genes = Crossover.two_point(parent1, parent2)
                elif CROSSOVER_METHOD == "uniform":
                    child1_genes, child2_genes = Crossover.uniform(parent1, parent2)
                elif CROSSOVER_METHOD == "granular":
                    child1_genes, child2_genes = Crossover.granular(parent1, parent2)
                else:
                    raise ValueError("Nieznana metoda krzyżowania!")
            else:
                # Jeśli krzyżowanie nie zachodzi, dzieci są kopiami rodziców
                child1_genes, child2_genes = parent1.genes[:], parent2.genes[:]

            # Tworzenie nowych chromosomów z przekazanymi genami
            child1 = Chromosome(len(child1_genes), LOWER_BOUND, UPPER_BOUND, genes=child1_genes)
            child2 = Chromosome(len(child2_genes), LOWER_BOUND, UPPER_BOUND, genes=child2_genes)

            # **Mutacja dzieci**
            if MUTATION_METHOD == "boundary":
                Mutation.boundary(child1)
                Mutation.boundary(child2)
            elif MUTATION_METHOD == "one_point":
                Mutation.one_point(child1, MUTATION_PROB)
                Mutation.one_point(child2, MUTATION_PROB)
            elif MUTATION_METHOD == "two_point":
                Mutation.two_point(child1, MUTATION_PROB)
                Mutation.two_point(child2, MUTATION_PROB)
            else:
                raise ValueError("Nieznana metoda mutacji!")

            # **Inwersja dzieci**
            Inversion.invert(child1, INVERSION_PROB)
            Inversion.invert(child2, INVERSION_PROB)

            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        # Zamiana starej populacji na nową
        population.individuals = new_population

        # Znalezienie najlepszego osobnika w populacji
        best_individual = population.get_best()
        best_values.append(best_individual.fitness)

        print(f"Generacja {generation+1}: Najlepszy osobnik: {best_individual}")

    return best_values  # Zwrócenie wartości funkcji celu do GUI lub zapisania wyników

# Jeśli skrypt jest uruchamiany bez GUI, uruchamiamy algorytm genetyczny i zapisujemy wyniki
if __name__ == "__main__":
    results = run_genetic_algorithm()

    # Rysowanie wykresu wyników
    import matplotlib.pyplot as plt
    plt.plot(range(len(results)), results, marker='o')
    plt.title("Wartość funkcji celu w kolejnych generacjach")
    plt.xlabel("Epoka")
    plt.ylabel("Najlepsza wartość funkcji")
    plt.grid()
    plt.show()
