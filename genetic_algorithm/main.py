import numpy as np
import random
from config import (
    POPULATION_SIZE, CHROMOSOME_LENGTH, NUM_GENERATIONS, LOWER_BOUND, UPPER_BOUND,
    SELECTION_METHOD, CROSSOVER_METHOD, CROSSOVER_PROB
)
from population import Population
from selection import Selection
from crossover import Crossover
from chromosome import Chromosome

# Przykładowa funkcja celu (Rastrigin)
def fitness_function(x):
    return - (10 * len(str(x)) + sum([(xi ** 2 - 10 * np.cos(2 * np.pi * xi)) for xi in [x]]))

# Inicjalizacja populacji
population = Population(POPULATION_SIZE, CHROMOSOME_LENGTH, LOWER_BOUND, UPPER_BOUND)

# Główna pętla algorytmu genetycznego
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
        new_population.append(Chromosome(len(child1_genes), LOWER_BOUND, UPPER_BOUND, genes=child1_genes))
        if len(new_population) < POPULATION_SIZE:
            new_population.append(Chromosome(len(child2_genes), LOWER_BOUND, UPPER_BOUND, genes=child2_genes))

    # Zamiana starej populacji na nową
    population.individuals = new_population

    # Znalezienie najlepszego osobnika w populacji
    best_individual = population.get_best()
    print(f"Generacja {generation+1}: Najlepszy osobnik: {best_individual}")
