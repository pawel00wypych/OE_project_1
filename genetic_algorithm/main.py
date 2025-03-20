import time
import sqlite3
from datetime import datetime
import os
import evaluation_functions
from genetic_algorithm.population import Population
from genetic_algorithm.selection import Selection
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.mutation import Mutation
from genetic_algorithm.inversion import Inversion
from genetic_algorithm.elitism import Elitism
from genetic_algorithm.config import POPULATION_SIZE, EPOCHS

global fitness_function, num_of_variables, mutation_probability
global crossover_probability, inversion_probability, variables_ranges_list
global precision, expected_minimum, db_name

def choose_function(fun_name):
    if fun_name == 'hypersphere':
        set_params_hypersphere()
    elif fun_name == 'hybrid':
        set_params_hybrid()

def set_params_hypersphere():
     # Hypersphere function to test -> 2 variables (x,y)

     global fitness_function, num_of_variables, mutation_probability
     global crossover_probability, inversion_probability, variables_ranges_list
     global precision, expected_minimum, db_name

     fitness_function = evaluation_functions.hypersphere_fitness
     num_of_variables = 2
     mutation_probability = 0.25
     crossover_probability = 0.7
     inversion_probability = 0.02
     variables_ranges_list=[(-5, 5)]
     precision = 6
     expected_minimum = evaluation_functions.get_hypersphere_minimum()
     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
     db_name = f"hypersphere_{timestamp}.db"

def set_params_hybrid():
    # Hybrid function to test

    global fitness_function, num_of_variables, mutation_probability
    global crossover_probability, inversion_probability, variables_ranges_list
    global precision, expected_minimum, db_name

    fitness_function = evaluation_functions.hybrid_fitness
    num_of_variables = 30
    mutation_probability = 0.25
    crossover_probability = 0.7
    inversion_probability = 0.02
    variables_ranges_list=[(-100, 100)]
    precision = 6
    expected_minimum = evaluation_functions.get_cec_hybrid_minimum()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_name = f"cec_hybrid_fun_1_{timestamp}.db"

def save_params_to_file(best_solution):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = "params"
    filename = f"params_{timestamp}.txt"
    file_path = os.path.join(directory, filename)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path,"w") as file:
        file.write(f"fitness_function:{fitness_function}\n")
        file.write(f"num_of_variables:{num_of_variables}\n")
        file.write(f"mutation_probability:{mutation_probability}\n")
        file.write(f"crossover_probability:{crossover_probability}\n")
        file.write(f"inversion_probability:{inversion_probability}\n")
        file.write(f"variables_ranges_list:{variables_ranges_list}\n")
        file.write(f"precision:{precision}\n")
        file.write(f"expected_minimum:{expected_minimum}\n")
        file.write(f"db_name:{db_name}\n")
        file.write(best_solution+"\n")


if __name__ == "__main__":
    choose_function("hypersphere")
    directory = "sqlite_folder"
    db_path = os.path.join(directory, db_name)

    if not os.path.exists(directory):
        os.makedirs(directory)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS epochs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fitness TEXT NOT NULL,
            variables TEXT NOT NULL,
            expected_result NOT NULL
        )
    ''')

    start_time = time.time()

    # Initialize population
    population = Population(num_of_variables, precision, variables_ranges_list * num_of_variables)
    # Initial evaluation
    population.evaluate(fitness_function)

    selected = Selection.tournament_selection(population, num_selected=POPULATION_SIZE)

    # We need this parameter to check if there is any improvement
    best_fitness = selected[0].fitness

    # Loop stop parameters
    no_improvement_counter = 0
    STOP_CRITERIA = EPOCHS  # Stop if there is no improvement for more than STOP_CRITERIA epochs

    for epoch in range(EPOCHS):
        print(f"Epoch {epoch + 1}/{EPOCHS}  best fitness = {best_fitness}")
        
        # Elite strategy
        elitism_operator = Elitism(population=population.individuals)
        elitism_operator.choose_the_best_individuals()
        elite_individuals = elitism_operator.get_elite_list()

        # Single point crossover
        crossover_operator = Crossover(population.individuals,crossover_probability, elitism_operator.number_of_elites)
        offspring = crossover_operator.single_point_crossover()

        # Single point mutation
        mutation_operator = Mutation(offspring, mutation_probability)
        mutated_offspring = mutation_operator.single_point_mutation()

        # Inversion
        for individual in mutated_offspring:
            Inversion.apply_inversion(individual, inversion_probability)


        # Population replacement
        new_population = elite_individuals + mutated_offspring
        population.individuals = new_population

        # Evaluation
        population.evaluate(fitness_function)

         # Tournament selection
        selected = Selection.tournament_selection(population, num_selected=POPULATION_SIZE)
        new_best_fitness = selected[0].fitness

        # Check if there is any improvement
        if new_best_fitness < best_fitness:
            best_fitness = new_best_fitness
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1

        cursor.execute("INSERT INTO epochs (fitness, variables, expected_result) VALUES (?, ?, ?)", (best_fitness, str(selected[0].decoded_variables),str(expected_minimum)))

        # End of evolution condition - check no-improvement counter
        if no_improvement_counter >= STOP_CRITERIA:
            print(f"Algorithm stopped – no improvement for {STOP_CRITERIA} epochs")
            break

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} s")
    print(f"Best solution: {selected[0].decoded_variables}, fitness value: {best_fitness}  best expected solution: {expected_minimum}")
    save_params_to_file(f"Best solution: {selected[0].decoded_variables}, fitness value: {best_fitness}  best expected solution: {expected_minimum}")
    conn.commit()
    conn.close()
