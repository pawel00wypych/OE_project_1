from benchmark_functions import Hypersphere, Rana # Sphere Function
from opfunu.cec_based.cec2014 import F12014, F282014   # Hybrid Function 1

# 📌 Sphere function - 2 variables
hypersphere_function = Hypersphere()


def hypersphere_fitness(variables):
    return hypersphere_function._evaluate(variables)

def get_hypersphere_minimum():
    return hypersphere_function.minimum()

def get_hypersphere_maximum():
    return hypersphere_function.maximum()

# rana function - 2 variables
rana_function = Rana()

def rana_fitness(variables):
    return rana_function._evaluate(variables)

def get_rana_minimum():
    return rana_function.minimum()

def get_rana_maximum():
    return rana_function.maximum()

# Composition function 6 F282014 - 30 variables
composition_6_function = F282014()

def composition_6_fitness(variables):
    return composition_6_function.evaluate(variables)

def get_cec_composition_6_minimum():
    return composition_6_function.f_global, tuple(composition_6_function.x_global)

# 📌 Hybrid Function 1 (Schwefel + Rastrigin + Elliptic)
hybrid_function = F12014()

def hybrid_fitness(variables):
    return hybrid_function.evaluate(variables)

def get_cec_hybrid_minimum():
    return hybrid_function.f_global, tuple(hybrid_function.x_global)