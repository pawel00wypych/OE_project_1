import time
import sqlite3
import os
from datetime import datetime
from statistics import mean, stdev

from genetic_algorithm.population import Population
from genetic_algorithm.selection import Selection
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.mutation import Mutation
from genetic_algorithm.inversion import Inversion
from genetic_algorithm.elitism import Elitism

def run_genetic_algorithm(config):
    fitness_function = config["fitness_function"]
    num_of_variables = config["num_of_variables"]
    mutation_probability = config["mutation_probability"]
    crossover_probability = config["crossover_probability"]
    inversion_probability = config["inversion_probability"]
    variables_ranges_list = config["variables_ranges_list"]
    precision = config["precision"]
    expected_minimum = config["expected_minimum"]
    selection_method = config["selection_method"]
    crossover_method = config["crossover_method"]
    mutation_method = config["mutation_method"]
    epochs = config["epochs"]
    population_size = config["population_size"]

    history = {
        "best_fitness": [],
        "avg_fitness": [],
        "std_fitness": [],
    }

    start_time = time.time()

    population = Population(num_of_variables, precision, variables_ranges_list * num_of_variables)
    population.size = population_size
    population.evaluate(fitness_function)

    selection_map = {
        "tournament": Selection.tournament_selection,
        "roulette": Selection.roulette_selection,
        "best": Selection.best_selection
    }

    crossover_map = {
        "single": Crossover.single_point_crossover,
        "two": Crossover.two_point_crossover,
        "uniform": Crossover.uniform_crossover,
        "granular": Crossover.granular_crossover
    }

    mutation_map = {
        "single": Mutation.single_point_mutation,
        "two": Mutation.two_point_mutation,
        "edge": Mutation.edge_mutation
    }

    for epoch in range(epochs):
        elitism_operator = Elitism(population=population.individuals)
        elitism_operator.choose_the_best_individuals()
        elite_individuals = elitism_operator.get_elite_list()

        crossover_operator = Crossover(population.individuals, crossover_probability, elitism_operator.number_of_elites)
        offspring = crossover_map[crossover_method](crossover_operator)

        mutation_operator = Mutation(offspring, mutation_probability)
        mutated_offspring = mutation_map[mutation_method](mutation_operator)

        for individual in mutated_offspring:
            Inversion.apply_inversion(individual, inversion_probability)

        new_population = elite_individuals + mutated_offspring
        population.individuals = new_population
        population.evaluate(fitness_function)

        fitness_values = [ind.fitness for ind in population.individuals]
        best_fitness = min(fitness_values)
        avg_fitness = mean(fitness_values)
        std_fitness = stdev(fitness_values) if len(fitness_values) > 1 else 0

        history["best_fitness"].append(best_fitness)
        history["avg_fitness"].append(avg_fitness)
        history["std_fitness"].append(std_fitness)

    end_time = time.time()
    execution_time = end_time - start_time

    best_individual = min(population.individuals, key=lambda ind: ind.fitness)

    result = {
        "best_solution": best_individual.decoded_variables,
        "best_fitness": best_individual.fitness,
        "expected_minimum": expected_minimum,
        "execution_time": execution_time,
        "history": history
    }

    return result
