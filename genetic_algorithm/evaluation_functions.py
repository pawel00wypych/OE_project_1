from benchmark_functions import Hypersphere # Sphere Function
from opfunu.cec_based.cec2014 import F12014  # Hybrid Function 1

# 📌 Sphere function - 2 variables
hypersphere_function = Hypersphere()
hypersphere_function_minimum = hypersphere_function.minima

def hypersphere_fitness(variables):
    return hypersphere_function._evaluate(variables)

# 📌 Hybrid Function 1 (Schwefel + Rastrigin + Elliptic)
hybrid_function = F12014()

def hybrid_fitness(variables):
    return hybrid_function.evaluate(variables)
