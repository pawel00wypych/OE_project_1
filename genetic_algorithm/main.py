import time
from genetic_algorithm.population import Population
from genetic_algorithm.selection import Selection
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.mutation import Mutation
from genetic_algorithm.inversion import Inversion
from genetic_algorithm.elitism import Elitism
from genetic_algorithm.config import POPULATION_SIZE, EPOCHS
from genetic_algorithm.evaluation_functions import hypersphere_fitness, hybrid_fitness
from benchmark_functions import Hypersphere # Sphere Function
hypersphere_function = Hypersphere()

# Hypersphere function to test -> 2 variables (x,y)
fitness_function = hypersphere_fitness
num_of_variables = 2
crossover_probability = 0.8
variables_ranges_list=[(-5, 5)]
precision = 5
expected_minimum = hypersphere_function.minimum()

# Hybrid function to test -> 2 variables (x,y)
# fitness_function = hypersphere_fitness
# num_of_variables = 2
# crossover_probability = 0.8
# variables_ranges_list=[(-5, 5)]
# precision = 5

if __name__ == "__main__":
    start_time = time.time()

    # Initialize population
    population = Population(num_of_variables, precision, variables_ranges_list * num_of_variables)
    # Initial evaluation
    population.evaluate(fitness_function)

    selected = Selection.tournament_selection(population, num_selected=POPULATION_SIZE, tournament_size=3)

    # We need this parameter to check if there is any improvement
    best_fitness = selected[0].fitness

    # Loop stop parameters
    no_improvement_counter = 0
    STOP_CRITERIA = EPOCHS  # Stop if there is no improvement for more than STOP_CRITERIA epochs

    for epoch in range(EPOCHS):
        print(f"Epoch {epoch + 1}/{EPOCHS}")
        
        # Elite strategy
        elitism_operator = Elitism(population=population.individuals)
        elitism_operator.choose_the_best_individuals()
        elite_individuals = elitism_operator.get_elite_list()

        # Single point crossover
        crossover_operator = Crossover(population.individuals,crossover_probability, elitism_operator.number_of_elites)
        offspring = crossover_operator.single_point_crossover()

        # Single point mutation
        mutation_operator = Mutation(offspring, mutation_probability=0.05)
        mutated_offspring = mutation_operator.single_point_mutation()

        # Inversion
        for individual in mutated_offspring:
            Inversion.apply_inversion(individual, inversion_probability=0.02)


        # Population replacement
        new_population = elite_individuals + mutated_offspring
        population.individuals = new_population

        # Evaluation
        population.evaluate(fitness_function)

         # Tournament selection
        selected = Selection.tournament_selection(population, num_selected=POPULATION_SIZE, tournament_size=3)
        new_best_fitness = selected[0].fitness

        # Check if there is any improvement
        if new_best_fitness < best_fitness:
            best_fitness = new_best_fitness
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1

        # End of evolution condition - check no-improvement counter
        if no_improvement_counter >= STOP_CRITERIA:
            print(f"Algorithm stopped – no improvement for {STOP_CRITERIA} epochs")
            break

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} s")
    print(f"Best solution: {selected[0].decoded_variables}, fitness value: {best_fitness}  best expected solution: {expected_minimum}")
