import tkinter as tk
from tkinter import ttk
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import *
from main import run_genetic_algorithm

class GeneticAlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorytm Genetyczny - Konfiguracja")
        self.root.geometry("500x700")

        # Parametry algorytmu
        self.params = {
            "Populacja": tk.IntVar(value=POPULATION_SIZE),
            "Epoki": tk.IntVar(value=NUM_GENERATIONS),
            "Mutacja [%]": tk.DoubleVar(value=MUTATION_PROB * 100),
            "Krzyżowanie [%]": tk.DoubleVar(value=CROSSOVER_PROB * 100),
            "Inwersja [%]": tk.DoubleVar(value=INVERSION_PROB * 100),
            "Elitizm": tk.IntVar(value=ELITISM_COUNT)
        }

        # Tworzenie interfejsu
        self.create_widgets()

    def create_widgets(self):
        # Nagłówek
        ttk.Label(self.root, text="Konfiguracja Algorytmu", font=("Arial", 14)).pack(pady=10)

        # Pola do ustawienia parametrów
        for label, var in self.params.items():
            frame = ttk.Frame(self.root)
            frame.pack(pady=5)
            ttk.Label(frame, text=label + ":").pack(side="left")
            ttk.Entry(frame, textvariable=var, width=10).pack(side="right")

        # Wybór funkcji testowej
        ttk.Label(self.root, text="Funkcja testowa:").pack(pady=5)
        self.test_function = ttk.Combobox(self.root, values=["rastrigin", "sphere", "ackley", "schwefel", "rosenbrock"])
        self.test_function.set(TEST_FUNCTION)
        self.test_function.pack(pady=5)

        # Wybór metody selekcji
        ttk.Label(self.root, text="Metoda selekcji:").pack(pady=5)
        self.selection_method = ttk.Combobox(self.root, values=["best", "roulette", "tournament"])
        self.selection_method.set(SELECTION_METHOD)
        self.selection_method.pack(pady=5)

        # Wybór metody krzyżowania
        ttk.Label(self.root, text="Metoda krzyżowania:").pack(pady=5)
        self.crossover_method = ttk.Combobox(self.root, values=["one_point", "two_point", "uniform", "granular"])
        self.crossover_method.set(CROSSOVER_METHOD)
        self.crossover_method.pack(pady=5)

        # Wybór metody mutacji
        ttk.Label(self.root, text="Metoda mutacji:").pack(pady=5)
        self.mutation_method = ttk.Combobox(self.root, values=["boundary", "one_point", "two_point"])
        self.mutation_method.set(MUTATION_METHOD)
        self.mutation_method.pack(pady=5)

        # Przycisk startu
        self.start_button = ttk.Button(self.root, text="Uruchom Algorytm", command=self.start_algorithm)
        self.start_button.pack(pady=20)

        # Wykres wyników
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.ax.set_title("Wartość funkcji celu")
        self.ax.set_xlabel("Epoka")
        self.ax.set_ylabel("Najlepsze rozwiązanie")
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(pady=20)

    def start_algorithm(self):
        """Rozpoczęcie algorytmu w osobnym wątku"""
        config_updates = {
            "POPULATION_SIZE": self.params["Populacja"].get(),
            "NUM_GENERATIONS": self.params["Epoki"].get(),
            "MUTATION_PROB": self.params["Mutacja [%]"].get() / 100,
            "CROSSOVER_PROB": self.params["Krzyżowanie [%]"].get() / 100,
            "INVERSION_PROB": self.params["Inwersja [%]"].get() / 100,
            "ELITISM_COUNT": self.params["Elitizm"].get(),
            "TEST_FUNCTION": self.test_function.get(),
            "SELECTION_METHOD": self.selection_method.get(),
            "CROSSOVER_METHOD": self.crossover_method.get(),
            "MUTATION_METHOD": self.mutation_method.get()
        }

        thread = threading.Thread(target=self.run_algorithm, args=(config_updates,))
        thread.start()

    def run_algorithm(self, config_updates):
        """Aktualizacja konfiguracji i uruchomienie algorytmu"""
        for key, value in config_updates.items():
            globals()[key] = value

        results = run_genetic_algorithm()

        # Rysowanie wykresu wyników
        self.ax.clear()
        self.ax.plot(range(len(results)), results, marker='o')
        self.ax.set_title("Wartość funkcji celu")
        self.ax.set_xlabel("Epoka")
        self.ax.set_ylabel("Najlepsze rozwiązanie")
        self.canvas.draw()

# Uruchomienie GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = GeneticAlgorithmGUI(root)
    root.mainloop()
