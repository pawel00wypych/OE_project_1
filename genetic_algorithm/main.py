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

def save_params_to_file(best_solution, config):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = "params"

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"params_{timestamp}.txt"
    file_path = os.path.join(directory, filename)



    with open(file_path,"w") as file:
        file.write(f"fitness_function:{config['fitness_function'].__name__}\n")
        file.write(f"num_of_variables:{config['num_of_variables']}\n")
        file.write(f"mutation_probability:{config['mutation_probability']}\n")
        file.write(f"crossover_probability:{config['crossover_probability']}\n")
        file.write(f"inversion_probability:{config['inversion_probability']}\n")
        file.write(f"variables_ranges_list:{config['variables_ranges_list']}\n")
        file.write(f"precision:{config['precision']}\n")
        file.write(f"expected_minimum:{config['expected_minimum']}\n")
        file.write(f"db_name:{config['fitness_function'].__name__}.db\n")
        file.write(best_solution+"\n")

def run_genetic_algorithm(config):

    directory = "sqlite_folder"

    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_name = f"{config['fitness_function'].__name__}_{timestamp}.db"
    db_path = os.path.join(directory, db_name)
    print(f"Database directory: {directory}")
    print(f"Database path: {db_path}")


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

    fitness_function = config["fitness_function"]
    num_of_variables = config["num_of_variables"]
    mutation_probability = config["mutation_probability"]
    crossover_probability = config["crossover_probability"]
    inversion_probability = config["inversion_probability"]
    inversion_level = config["inversion_level"]
    variables_ranges_list = config["variables_ranges_list"]
    precision = config["precision"]
    expected_minimum = config["expected_minimum"]
    selection_method = config["selection_method"]
    selection_type = config["selection_type"] # min or max
    crossover_method = config["crossover_method"]
    mutation_method = config["mutation_method"]
    epochs = config["epochs"]
    population_size = config["population_size"]
    stop_criteria = config["stop_criteria"]

    history = {
        "best_fitness": [],
        "avg_fitness": [],
        "std_fitness": [],
    }

    start_time = time.time()

    # Initialize population
    population = Population(num_of_variables, precision, variables_ranges_list * num_of_variables)
    population.size = population_size

    # Initial evaluation
    population.evaluate(fitness_function)


    selection_map = {
        "tournament": Selection.tournament_selection,
        "roulette": Selection.roulette_selection,
        "best": Selection.best_selection
    }

    crossover_map = {
        "single": Crossover.single_point_crossover,
        "two": Crossover.two_point_crossover,
        "granular": Crossover.granular_crossover,
        "uniform": Crossover.uniform_crossover
    }

    mutation_map = {
        "single": Mutation.single_point_mutation,
        "two": Mutation.two_point_mutation,
        "edge": Mutation.edge_mutation
    }

    selected = selection_map[selection_method](population, selection_type = selection_type, num_selected=population.size) # selection_type <- min or max
    best_fitness = selected[0].fitness

    # Loop stop parameters
    no_improvement_counter = 0
    STOP_CRITERIA = stop_criteria # Stop if there is no improvement for more than STOP_CRITERIA epochs

    for epoch in range(epochs):

        # Elite strategy
        elitism_operator = Elitism(population=population.individuals)
        elitism_operator.choose_the_best_individuals()
        elite_individuals = elitism_operator.get_elite_list()

        # Crossover
        crossover_operator = Crossover(population.individuals, crossover_probability, elitism_operator.number_of_elites)
        offspring = crossover_map[crossover_method](crossover_operator)  # Equivalent to: offspring = crossover_operator.single_point_crossover()

        # Mutation
        mutation_operator = Mutation(offspring, mutation_probability)
        mutated_offspring = mutation_map[mutation_method](mutation_operator)

        # Inversion
        for individual in mutated_offspring:
            Inversion.apply_inversion(individual, inversion_probability, inversion_level)

        # Population replacement
        new_population = elite_individuals + mutated_offspring
        population.individuals = new_population

        # Evaluation
        population.evaluate(fitness_function)

        # Selection
        selected = selection_map[selection_method](population, selection_type = selection_type, num_selected=population.size) # selection_type <- min or max
        new_best_fitness = selected[0].fitness

        # Check if there is any improvement
        if selection_type == "min":
            print("min")
            if new_best_fitness < best_fitness:
                best_fitness = new_best_fitness
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1
        elif selection_type == "max":
            print("max")

            if new_best_fitness > best_fitness:
                best_fitness = new_best_fitness
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1


        fitness_values = [ind.fitness for ind in population.individuals]
        avg_fitness = mean(fitness_values)
        std_fitness = stdev(fitness_values) if len(fitness_values) > 1 else 0

        cursor.execute("INSERT INTO epochs (fitness, variables, expected_result) VALUES (?, ?, ?)",(best_fitness, str(selected[0].decoded_variables), str(expected_minimum)))

        print(f"Epoch {epoch} best solution: {selected[0].decoded_variables}, fitness value: {best_fitness}  best expected solution: {expected_minimum}")

        history["best_fitness"].append(best_fitness)
        history["avg_fitness"].append(avg_fitness)
        history["std_fitness"].append(std_fitness)

        if no_improvement_counter >= STOP_CRITERIA:
            print(f"Algorithm stopped – no improvement for {STOP_CRITERIA} epochs")
            break

    end_time = time.time()
    execution_time = end_time - start_time

    result = {
        "best_solution": selected[0].decoded_variables,
        "best_fitness": best_fitness,
        "expected_minimum": expected_minimum,
        "execution_time": execution_time,
        "history": history
    }

    save_params_to_file(f"Best solution: {selected[0].decoded_variables}, fitness value: {best_fitness}  best expected solution: {expected_minimum}", config)
    conn.commit()
    conn.close()

    return result
