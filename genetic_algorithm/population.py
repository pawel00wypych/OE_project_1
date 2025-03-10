from config import POPULATION_SIZE

class Population:
    def _init(self):
    #Tworzenie populacji 
        self.size = POPULATION_SIZE #Pobranie wartosci populacji z config
        self.individuals = []   #Lista do przechowywania osobników

    def initialization(self):
        for _ in range(self.size):
            self.individuals.append("Osobnik") #Narazie jakiś zastępczu

    def get_size_population(self):
        return len(self.individuals)  #Zwrócenie liczby osobnikow w populacji

