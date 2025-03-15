from population import Population
from config import MAX_GENERATIONS

pop = Population(number_of_variables=10, precision=3, variables_list=[(-5,5)]*10, function_name="sphere")

# Algorytm genetyczny - główna pętla
for generation in range(MAX_GENERATIONS):
    pop.evaluate()  # Ocena fitness populacji
    pop.select()    # Selekcja rodziców
    pop.crossover() # Krzyżowanie
    pop.mutate()    # Mutacja
    pop.apply_elitism()  # Strategia elitarna

    # Pobranie najlepszego osobnika w tej generacji
    best = pop.get_best()
    print(f"Generacja {generation+1}: Najlepszy wynik = {best.fitness}")

print("Optymalizacja zakończona.")
