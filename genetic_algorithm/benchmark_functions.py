from benchmark_functions import Hypersphere # Sphere Function
from opfunu.cec_based.cec2014 import F12014  # Hybrid Function 1

# 📌 Sphere function
sphere_function = Hypersphere()

def sphere_fitness(variables):
    return sphere_function.evaluate(variables)

# 📌 Hybrid Function 1 (Schwefel + Rastrigin + Elliptic)
hybrid_function = F12014()

def hybrid_fitness(variables):
    return hybrid_function.evaluate(variables)
