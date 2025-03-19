import time
from genetic_algorithm.population import Population
from genetic_algorithm.selection import Selection
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.mutation import Mutation
from genetic_algorithm.inversion import Inversion
from genetic_algorithm.elitism import Elitism
from genetic_algorithm.config import POPULATION_SIZE, EPOCHS
from genetic_algorithm.evaluation_functions import hypersphere_fitness, hybrid_fitness

# Hypersphere function to test -> 2 variables (x,y)
fitness_function = hypersphere_fitness
num_of_variables = 2

if __name__ == "__main__":
    start_time = time.time()

    # Initialize population
    population = Population(number_of_variables=num_of_variables, precision=5, variables_ranges_list=[(-5, 5)] * num_of_variables)
    # Initial evaluation
    population.evaluate(fitness_function)

    best_individuals_after_selection = Selection.tournament_selection(population, num_selected=POPULATION_SIZE, tournament_size=3)

    best_fitness = best_individuals_after_selection.fitness

    # Loop stop parameters
    no_improvement_counter = 0
    STOP_CRITERIA = 10  # Stop if there is no improvement for more than STOP_CRITERIA epochs

    for epoch in range(EPOCHS):
        print(f"Epoch {epoch + 1}/{EPOCHS}")
        
        # Elite strategy
        elitism_operator = Elitism(population=population.individuals)
        elitism_operator.choose_the_best_individuals()
        elite_individuals = elitism_operator.get_elite_list()

        # Krzyżowanie jednopunktowe
        crossover_operator = Crossover(selected, crossover_probability=0.7)
        offspring = crossover_operator.single_point_crossover()

        # Mutacja jednopunktowa
        mutation_operator = Mutation(offspring, mutation_probability=0.05)
        mutated_offspring = mutation_operator.single_point_mutation()

        # Inwersja
        for individual in mutated_offspring:
            Inversion.apply_inversion(individual, inversion_probability=0.02)


        # Aktualizacja populacji
        new_population = elite_individuals + mutated_offspring[:POPULATION_SIZE - len(elite_individuals)]
        population.individuals = new_population
        population.evaluate(fitness_function)

         # Selekcja turniejowa
        selected = Selection.tournament_selection(population, num_selected=POPULATION_SIZE, tournament_size=3)

        # Sprawdzamy, czy jest poprawa
        new_best = max(selected)
        if new_best.fitness > best_fitness:
            best_fitness = new_best.fitness
            no_improvement_counter = 0  # Reset stagnacji
        else:
            no_improvement_counter += 1

        # Warunek stopu – jeśli nie ma poprawy przez N epok, zatrzymujemy
        if no_improvement_counter >= STOP_CRITERIA:
            print(f"Zatrzymano algorytm – brak poprawy przez {STOP_CRITERIA} epok")
            break

    # Pomiar czasu wykonania
    end_time = time.time()
    print(f"Czas wykonania: {end_time - start_time:.2f} s")
    print(f"Najlepsze rozwiązanie: {best_individuals.decoded_variables}, wartość: {best_fitness}")
