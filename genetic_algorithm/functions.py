import numpy as np

class TestFunctions:
    @staticmethod
    def rastrigin(x):
        """Funkcja Rastrigina – ma wiele minimów lokalnych, trudna do optymalizacji."""
        return 10 * len(x) + sum([(xi ** 2 - 10 * np.cos(2 * np.pi * xi)) for xi in x])

    @staticmethod
    def sphere(x):
        """Funkcja Sphere – najprostsza, ma jedno globalne minimum."""
        return sum([xi ** 2 for xi in x])

    @staticmethod
    def ackley(x):
        """Funkcja Ackley – kombinacja sinusoidalnych oscylacji i eksponencjalnej funkcji."""
        a = 20
        b = 0.2
        c = 2 * np.pi
        d = len(x)
        sum1 = sum([xi ** 2 for xi in x])
        sum2 = sum([np.cos(c * xi) for xi in x])
        return -a * np.exp(-b * np.sqrt(sum1 / d)) - np.exp(sum2 / d) + a + np.e

    @staticmethod
    def schwefel(x):
        """Funkcja Schwefela – minima są daleko od zera, co utrudnia optymalizację."""
        return 418.9829 * len(x) - sum([xi * np.sin(np.sqrt(abs(xi))) for xi in x])

    @staticmethod
    def rosenbrock(x):
        """Funkcja Rosenbrocka – trudna do optymalizacji z wąską doliną prowadzącą do minimum."""
        return sum([100 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1) ** 2 for i in range(len(x) - 1)])
