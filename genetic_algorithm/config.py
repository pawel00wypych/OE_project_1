# Konfiguracja algorytmu genetycznego

# Liczba osobników w populacji
POPULATION_SIZE = 100  

# Długość chromosomu (liczba bitów na zmienną)
CHROMOSOME_LENGTH = 20  

# Liczba epok (iteracji)
NUM_GENERATIONS = 200  

# Prawdopodobieństwo krzyżowania
CROSSOVER_PROB = 0.8  

# Prawdopodobieństwo mutacji
MUTATION_PROB = 0.05  

# Prawdopodobieństwo inwersji
INVERSION_PROB = 0.02  

# Liczba najlepszych osobników przechodzących do kolejnej populacji (elitism)
ELITISM_COUNT = 5  

# Rodzaj selekcji ("best", "roulette", "tournament")
SELECTION_METHOD = "roulette"  

# Rodzaj krzyżowania ("one_point", "two_point", "uniform", "granular")
CROSSOVER_METHOD = "one_point"  

# Rodzaj mutacji ("boundary", "one_point", "two_point")
MUTATION_METHOD = "one_point"  

# Funkcja testowa do optymalizacji (np. "rastrigin", "ackley")
TEST_FUNCTION = "rastrigin"  

# Dolna i górna granica przedziału zmiennych
LOWER_BOUND = -5.0
UPPER_BOUND = 5.0

# Rodzaj selekcji ("best", "roulette", "tournament")
SELECTION_METHOD = "roulette"

# Prawdopodobieństwo krzyżowania
CROSSOVER_PROB = 0.8  

# Rodzaj krzyżowania ("one_point", "two_point", "uniform", "granular")
CROSSOVER_METHOD = "one_point"  