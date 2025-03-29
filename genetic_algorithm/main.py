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
from genetic_algorithm import evaluation_functions

def save_params_to_file(result, config):
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
        file.write(f"expected_result:{config['expected_minimum']}\n")
        file.write(f"db_name:{config['fitness_function'].__name__}.db\n")
        file.write(f"number of executions:{config['num_of_executions']}\n")
        file.write(f"best_fitness: {result['best_fitness']} \n")
        file.write(f"best_solution: {result['best_solution']} \n")
        file.write(f"best_execution_num: {result['best_execution_num']} \n")
        file.write(f"worst_fitness: {result['worst_fitness']} \n")
        file.write(f"worst_solution: {result['worst_solution']} \n")
        file.write(f"worst_execution_num: {result['worst_execution_num']} \n")
        file.write(f"execution_time: {result['execution_time']} \n")
        file.write(f"error: {result['error']} \n")

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
                execution_num INTEGER NOT NULL,
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
    number_of_executions = config["num_of_executions"]

    history = {
        "best_fitness": [],
        "avg_fitness": [],
        "std_fitness": [],
        "error": [],
        "best_fitness_variables": [],
        "execution_num": [],

    }

    start_time = time.time()

    for i in range(1,number_of_executions+1):
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
                if new_best_fitness < best_fitness:
                    best_fitness = new_best_fitness
                    no_improvement_counter = 0
                else:
                    no_improvement_counter += 1
            elif selection_type == "max":
                if new_best_fitness > best_fitness:
                    best_fitness = new_best_fitness
                    no_improvement_counter = 0
                else:
                    no_improvement_counter += 1


            fitness_values = [ind.fitness for ind in population.individuals]
            avg_fitness = mean(fitness_values)
            std_fitness = stdev(fitness_values) if len(fitness_values) > 1 else 0
            error = abs(expected_minimum[0] - best_fitness)


            cursor.execute("INSERT INTO epochs (execution_num, fitness, variables, expected_result) VALUES (?,?, ?, ?)",(i, best_fitness, str(selected[0].decoded_variables), str(expected_minimum)))

            print(f"Execution: {i} epoch: {epoch} best solution: {selected[0].decoded_variables}, fitness value: {best_fitness}  best expected solution: {expected_minimum} error: {error}")

            history["best_fitness"].append(best_fitness)
            history["best_fitness_variables"].append(selected[0].decoded_variables)
            history["avg_fitness"].append(avg_fitness)
            history["std_fitness"].append(std_fitness)
            history["error"].append(error)
            history["execution_num"].append(i)

            if no_improvement_counter >= STOP_CRITERIA:
                print(f"Algorithm stopped – no improvement for {STOP_CRITERIA} epochs")
                break

    end_time = time.time()
    execution_time = end_time - start_time

    # find the best fitness from the bests fitnesses from all executions and the worst fitness from the best fitnesses
    best_fitness_of_all_executions = best_fitness
    best_solution_of_all_executions = selected[0].decoded_variables
    best_execution_num = 0
    worst_fitness_of_best = best_fitness
    worst_solution_of_best = selected[0].decoded_variables
    worst_of_best_execution_num = 0

    if selection_type == "min":
        best_fitness_of_all_executions = min(history["best_fitness"])
        best_index = history["best_fitness"].index(best_fitness_of_all_executions)
        best_solution_of_all_executions = history["best_fitness_variables"][best_index]
        best_execution_num = history["execution_num"][best_index]

        worst_fitness_of_best = max(history["best_fitness"])
        worst_index = history["best_fitness"].index(worst_fitness_of_best)
        worst_solution_of_best = history["best_fitness_variables"][worst_index]
        worst_of_best_execution_num = history["execution_num"][worst_index]
    elif selection_type == "max":
        best_fitness_of_all_executions = max(history["best_fitness"])
        best_index = history["best_fitness"].index(best_fitness_of_all_executions)
        best_solution_of_all_executions = history["best_fitness_variables"][best_index]
        best_execution_num = history["execution_num"][best_index]

        worst_fitness_of_best = min(history["best_fitness"])
        worst_index = history["best_fitness"].index(worst_fitness_of_best)
        worst_solution_of_best = history["best_fitness_variables"][worst_index]
        worst_of_best_execution_num = history["execution_num"][worst_index]


    result = {
        "best_solution": best_solution_of_all_executions,
        "best_fitness": best_fitness_of_all_executions,
        "worst_solution": worst_solution_of_best,
        "worst_fitness": worst_fitness_of_best,
        "error": sum(history["error"])/number_of_executions,
        "expected_minimum": expected_minimum,
        "execution_time": execution_time/number_of_executions,
        "num_of_executions": number_of_executions,
        "best_execution_num": best_execution_num,
        "worst_execution_num": worst_of_best_execution_num,
        "history": history
    }

    save_params_to_file(result,
                        config)
    conn.commit()
    conn.close()

    return result


if __name__ == "__main__":
    fitness = evaluation_functions.hypersphere_fitness
    expected = evaluation_functions.get_hypersphere_minimum()

    config = {
        "fitness_function": fitness,
        "expected_minimum": expected,
        "num_of_variables": 2,
        "variables_ranges_list": [(-5, 5)],
        "precision": 6,
        "mutation_probability": 0.7,
        "crossover_probability": 0.5,
        "inversion_probability": 0.3,
        "inversion_level": 0.2,
        "selection_method": "tournament",
        "selection_type": "min",
        "crossover_method": "two",
        "mutation_method": "two",
        "epochs": 100,
        "population_size": 100,
        "stop_criteria": 100,
        "num_of_executions": 10
    }

    run_genetic_algorithm(config)